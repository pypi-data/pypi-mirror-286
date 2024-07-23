"""Handling of the rules, procedures and algorithms for a particular KEP.
"""

from collections import defaultdict
import logging
from time import thread_time
from typing import Callable, Iterable, MutableMapping, Optional
import random

from kep_solver.entities import (
    Instance,
    Donor,
    Recipient,
    Status,
    Participant,
    DynamicInstance,
    Transplant,
    KEPDataValidationException,
)
from kep_solver.model import Objective, Model, CycleAndChainModel
from kep_solver.graph import Exchange, CompatibilityGraph


logger = logging.getLogger(__name__)


class ModelledExchange:
    """An exchange as modelled, including its value for various
    objectives and any other relevant information.
    """

    def __init__(self, exchange: Exchange, values: list[float]):
        """Constructor for ModelledExchange. Contains the Exchange object, and
        also the value of this exchange for the various objectives in this
        model.

        :param exchange: The exchange
        :param values: The value of this exchange for each objective
        """
        self._exchange = exchange
        self._values = values

    @property
    def exchange(self) -> Exchange:
        """The underlying exchange."""
        return self._exchange

    @property
    def values(self) -> list[float]:
        """The values of this exchange."""
        return self._values

    def __len__(self) -> int:
        """The number of transplants in the underlying exchange."""
        return len(self._exchange)

    def __str__(self) -> str:
        """A human-readable representation of this exchange."""
        return f"ModelledExchange({str(self._exchange)})"

    def __repr__(self) -> str:
        return str(self)


class Solution:
    """A solution to one instance of a KEP. Contains the exchanges, and
    the set of objective values attained.
    """

    def __init__(
        self,
        exchanges: list[ModelledExchange],
        scores: list[float],
        possible: list[ModelledExchange],
        times: list[tuple[str, float]],
        numSolutions: list[int],
    ):
        """Constructor for Solution. This class essentially just stores
        any information that may be useful.

        :param exchanges: the list of selected exchanges
        :param scores: the list of scores achieved for each objective
        :param possible: the set of possible exchanges, and their
            values for each objective
        :param times: The time taken for various operations. Each is a
            tuple with a string description of the action, and the time
            (in seconds)
        :param numSolutions: Either an empty list (if solutions weren't
            counted) or a list such that the i'th entry in the list is the
            number of distinct solutions found for the i'th objective
        """
        self._selected: list[ModelledExchange] = exchanges
        self._values: list[float] = scores
        self._possible: list[ModelledExchange] = possible
        self._times: list[tuple[str, float]] = times
        self._numSolutions = numSolutions

    @property
    def times(self) -> list[tuple[str, float]]:
        """Get the time taken for various operations. Each element of
        the returned list is a tuple where the first item is a string
        description of some operation, and the second item is the time
        taken in seconds.

        :return: the list of times (and their descriptions)
        """
        return self._times

    @property
    def selected(self) -> list[ModelledExchange]:
        """Get the selected solution.

        :return: the list of exchanges selected.
        """
        return self._selected

    @property
    def values(self) -> list[float]:
        """Get the Objective values of the selected solution.

        :return: the list of objective values
        """
        return self._values

    @property
    def possible(self) -> list[ModelledExchange]:
        """Return a list of all the possible chains and cycles that may
        be selected as ModelledExchange objects that contain the value of said
        exchange for each objective.

        :return: a list of cycles/chains as ModelledExchange objects
        """
        return self._possible

    @property
    def numSolutions(self) -> list[int]:
        """Return the number of optimal solutions found for each objective.

        :return: a list of cycles/chains as ModelledExchange objects
        """
        if not self._numSolutions:
            raise Exception("Error: Number of solutions was not calculated.")
        return self._numSolutions


class Programme:
    """A kidney exchange programme (or more specifically, the objectives and
    parameters for a KEP)."""

    def __init__(
        self,
        objectives: list[Objective],
        maxCycleLength: int,
        maxChainLength: int,
        description: str,
        build_alt_embed: int = 0,
        full_details: bool = True,
        model: type[Model] = CycleAndChainModel,
    ):
        """Constructor for Programme. This represents a set of objectives, and
        parameters for running matchings (such as maximum cycle and chain
        lengths).

        :param objectives: the list of objectives
        :param maxCycleLength: The longest cycle length allowed.
        :param maxChainLength: The longest chain length allowed. Note that the
            length of a chain includes the non-directed donor.
        :param description: A description of this programme.
        :param build_alt_embed: Whether to build alternate and embedded
            exchanges. build_alt_embed can be set to any of the following:

            0. Don't build alternate and embedded cycles. Faster, if you don't need alternate and embedded cycles
            1. Build all alternate and embedded cycles.
            2. Build only those alternate and embedded cycles that NHSBT expects
            3. Build only those alternate and embedded cycles that NHSBT expects, where embedded exchanges cannot use new donors
        :param full_details: If True, try to return details for all possible
            exchanges (even the ones not selected). Note that this will fail on
            some models that don't enumerate all possible exchnages.
        """
        # Create a copy of the list of objectives with the magic colon
        self._objectives: list[Objective] = objectives[:]
        self._maxCycleLength: int = maxCycleLength
        self._maxChainLength: int = maxChainLength
        self._full_details: bool = full_details
        self._description: str = description
        self._build_alt_embed = build_alt_embed
        self._modelClass = model

    @property
    def build_alternates_and_embeds(self) -> bool:
        """Will this programme build alternate and embedded exchanges."""
        return self._build_alt_embed != 0

    @property
    def description(self) -> str:
        """A description of this programme."""
        return self._description

    @description.setter
    def description(self, desc) -> None:
        """A description of this programme."""
        self._description = desc

    @property
    def objectives(self) -> list[Objective]:
        """The list of objectives for this Programme."""
        return self._objectives

    @property
    def maxCycleLength(self) -> int:
        """The maximum length of cycles in this programme."""
        return self._maxCycleLength

    @property
    def maxChainLength(self) -> int:
        """The maximum length of chains in this programme. Note that this includes
        the non-directed donor, so a chain of length 1 only has a non-directed
        donor and no recipients."""
        return self._maxCycleLength

    def getOptimal(
        self, exchanges: list[Exchange], graph: CompatibilityGraph
    ) -> Exchange | None:
        """Given a list of exchanges, return an optimal exchange, where
        optimality is determined by the objectives used.

        :param exchanges: The list of exchanges to consider
        :param graph: The compatibility graph for these exchanges
        :return: An optimal exchange. If there are multiple exchanges that are
            all optimal, the first such exchange in the list is returned.
        """
        kept: list[Exchange] = exchanges
        for objective in self.objectives:
            best: float | None = None
            for exchange in kept:
                value = objective.value(graph, exchange)
                if best is None or value > best:
                    best = value
                    kept = [exchange]
                elif value == best:
                    kept.append(exchange)
        if kept:
            # We're just choosing one arbitrarily at this point
            return kept[0]
        return None

    def solve_single(
        self,
        instance: Instance,
        *,
        maxCycleLength: Optional[int] = None,
        maxChainLength: Optional[int] = None,
        countSolutions: bool = False,
        maxCount: Optional[list[int]] = None,
        solver=None,
    ) -> tuple[Optional[Solution], Model]:
        """Run a single instance through this programme, returning the solution, or
        None if no solution is found (e.g., if the solver crashes).

        :param instance: The instance to solve
        :param maxCycleLength: The longest cycle allowed. If not specified, we
            use the default from the Programme
        :param maxChainLength: The longest chain allowed. If not specified, we
            use the default from the Programme
        :param solver: An instantiated PuLP solver. If empty, a CBC solver is
            created and used
        :return: A tuple containing a Solution object, or None if an error
            occured, as well as the model that was solved.
        """
        if maxCycleLength is None:
            maxCycleLength = self._maxCycleLength
        if maxChainLength is None:
            maxChainLength = self._maxChainLength
        t = thread_time()
        model = self._modelClass(
            instance,
            self._objectives,
            maxChainLength=maxChainLength,
            maxCycleLength=maxCycleLength,
            build_alt_embed=self._build_alt_embed,
        )
        solution, times, numSolutions = model.solve(countSolutions, maxCount, solver)
        times.append(("Total time", thread_time() - t))
        if solution is None:
            return None
        values = model.objective_values
        if self._full_details:
            exchange_values: dict[Exchange, list[float]] = {
                exchange: model.exchange_values(exchange)
                for exchange in model.exchanges
            }
            solutions = [ModelledExchange(ex, exchange_values[ex]) for ex in solution]
            possible = [
                ModelledExchange(ex, exchange_values[ex])
                for ex in exchange_values.keys()
            ]
            return Solution(solutions, values, possible, times, numSolutions), model
        else:
            solutions = [
                ModelledExchange(ex, model.exchange_values(ex)) for ex in solution
            ]
            return Solution(solutions, values, [], times, numSolutions), model


"""A data class for functions that take as input the current period, as well as
all donors and recipients and returns True if and only if a match run should
occur in the given period.
"""
MatchRunScheduleFunction = Callable[
    [
        int,
        Iterable[Recipient],
        Iterable[Donor],
    ],
    bool,
]


class DynamicSimulation:
    def __init__(
        self,
        programme: Programme,
        periods: int,
        dynamic_instance: DynamicInstance,
        match_run_fn: MatchRunScheduleFunction,
        scheduler: Callable[[Exchange], int],
        allow_bridge_donors: bool = False,
        bridge_donor_attrition: Callable[[Donor], float] = lambda x: 0.0,
        recourse: str = "Internal",
    ):
        """Create a simulation from the given parameters. Note that this will
        change the status of every recipient and donor to NotYetArrived.

        :param programme: The Programme to use for optimisation.
        :param periods: How many periods to simulate.
        :param instance: The dynamic instance containing donors, recipients,
            and transplants, and details on when people arrive, depart, become
            ill, and information on which transplants will fail a laboratory
            crossmatch.
        :param match_run_fn: A function that takes as input the current period,
            as well as all DynamicParticipants and returns True if and only if
            a match run should occur in the given period
        :param scheduler: A function that takes as input an Exchange, and
            returns an int such that this exchange would be attempted in that
            many periods time
        :param allow_bridge_donors: If True, the last donor in a chain becomes
            a bridge donor for the next period, acting like a new non-directed
            donor.
        :param bridge_donor_attrition: A function that takes as input a bridge
            donor, and returns the chance of attrition of this donor in a given
            period. The default is that bridge donors never leave due to
            attrition.
        :param recourse: One of "Internal" or "None" (specifically, the string
            "None" and not the Python type None). If "Internal" then if an
            exchange fails, we attempt to find an exchange using a (not
            necessarily strict) subset of the same participants. If "None", the
            exchange is allowed to fail and no recourse occurs.

        """
        self._instance = dynamic_instance
        self.allow_bridge_donors = allow_bridge_donors
        self.periods = periods
        self.match_run_fn = match_run_fn
        self.programme = programme
        self.scheduler = scheduler
        self.bridge_donor_attrition = bridge_donor_attrition
        self._recourse = recourse
        self.reset()

    def _match_run(
        self,
        period: int,
        bridge_donors: list[Donor],
    ) -> tuple[Solution, Model, Instance]:
        """Create the instance for this period and then solve it. Returns a
        tuple containing the solution to the instance, and the instance itself.

        :param period: The time period, needed to check illness and departures
        :param bridge_donors: The bridge donors for this match run
        :return: A tuple containing the solution to the instance, and the
            instance itself.
        """
        this_run = Instance()
        for r in self._instance.activeRecipients():
            # This also adds their paired donors, so only add NDDs in next loop
            this_run.addRecipient(r)
        for thing in [self._instance.donors.values(), bridge_donors]:
            for donor in thing:
                if donor.NDD and donor.status == Status.InPool:
                    this_run.addDonor(donor)
        for t in self._instance.transplants:
            if (
                this_run.hasDonor(t.donor)
                and this_run.hasRecipient(t.recipient)
                and not t.known_to_fail
            ):
                this_run.addTransplant(t)
        solution, model = self.programme.solve_single(this_run)
        if not solution:
            raise Exception("No solution found.")
        return solution, model, this_run

    def _handle_arrival_attrition(
        self,
        period: int,
        bridge_donors: list[Donor],
    ) -> list[Donor]:
        """Check arrival and attrition for participants. If period is arrival
        time, then the participant has arrived, otherwise if the period is
        equal to or greater than the departure time, the participant has left.
        This does mean that if arrival time and departure time are equal, the
        participant will be not ever be present.

        :param period: The current time period
        :param bridge_donors: A list of the bridge donors
        """
        for recipient in self._instance.allRecipients():
            if recipient.id not in self._instance.recipient_arrivals:
                continue
            if (
                period == self._instance.recipient_arrivals[recipient.id]
                and period != self._instance.recipient_departures[recipient.id]
                and recipient.status == Status.NotYetArrived
            ):
                recipient.status = Status.InPool
                for donor in recipient.donors():
                    donor.status = Status.InPool
            elif period >= self._instance.recipient_departures[
                recipient.id
            ] and recipient.status in [
                Status.InPool,
                Status.Selected,
            ]:
                recipient.status = Status.Left
        for ndd in self._instance.allNDDs():
            if ndd.id not in self._instance.ndd_arrivals:
                continue
            if (
                period == self._instance.ndd_arrivals[ndd.id]
                and period != self._instance.ndd_departures[ndd.id]
                and ndd.status == Status.NotYetArrived
            ):
                ndd.status = Status.InPool
            elif period >= self._instance.ndd_departures[ndd.id] and ndd.status in [
                Status.InPool,
                Status.Selected,
            ]:
                ndd.status = Status.Left
        # Extra attrition of bridge donors
        return [
            donor
            for donor in bridge_donors
            if random.random() > self.bridge_donor_attrition(donor)
        ]

    def _find_substitute(
        self,
        exchange: Exchange,
        graph: CompatibilityGraph,
        *,
        participants: list[Participant] = [],
        transplants: list[Transplant] = [],
    ) -> Exchange | None:
        """Attempt to find an substitute (alternate or embedded) exchange for
        the given one. The new exchange should not include the given dynamic
        participant.

        :param exchange: The exchange which is failing
        :param participants: The participants who are unable to take part in
            this exchange
        :param transplants: The transplants that are not viable in this exchange
        :param graph: The compatibility graph used to find this exchange
        :return: A new exchange without the given participant, or None if no
            substitute is found.
        """
        # Return the participants to the pool
        self._return_to_pool(exchange)
        if self._recourse == "None":
            return None
        if self.programme.build_alternates_and_embeds:
            substitutes = list(
                exchange
                for exchange in exchange.alternates + exchange.embedded
                if not any(
                    exchange.hasParticipant(participant) for participant in participants
                )
                and not any(
                    self._instance.getTransplant(donor, recipient).known_to_fail
                    for donor, recipient in exchange.transplantPairs()
                )
            )
            return self.programme.getOptimal(
                substitutes,
                graph,
            )
        instance = Instance()
        for recipient in exchange.allRecipients():
            if recipient not in participants:
                instance.addRecipient(recipient)
        for donor in exchange.allDonors():
            if donor.NDD and donor not in participants:
                instance.addDonor(donor)
        solution, model = self.programme.solve_single(instance)
        if solution is None or not solution.selected:
            return None
        return solution.selected[0].exchange

    def _perform_exchange(
        self,
        exchange: Exchange,
        period: int,
        graph: CompatibilityGraph,
    ) -> tuple[Exchange | None, list[Transplant], Optional[Donor]]:
        """Attempt to perform an exchange.

        :param exchange: The exchange in question
        :param period: The time period, needed to check illness and departures
        :param graph: The compatibility graph used to find this exchange
        :return: A tuple containing the performed exchange (which may be
            different to the input exchange if recourse is used, and may be
            None if no exchange is performed) , a list of the transplants that
            are now known to either be failing or not-failing, and a
            DynamicParticipant object if a new bridge donor is created.
        """
        # attempt to perform
        for pair in exchange.allPairs():
            participant: Participant
            if pair[1] is None:
                participant = pair[0]
            else:
                participant = pair[1]
            if (
                self._instance.is_ill(participant, period)
                or participant.status == Status.Left
            ):
                if alternate := self._find_substitute(
                    exchange, graph, participants=[participant]
                ):
                    return self._perform_exchange(alternate, period, graph)
                # Skipping this exchange due to illness or person leaving
                return None, [], None
        # Get transplants
        transplants = [
            self._instance.getTransplant(donor, recipient)
            for donor, recipient in exchange.transplantPairs()
        ]
        # check for real xmatch
        failed: list[Transplant] = []
        for t in transplants:
            if t in self._instance.failing_transplants:
                t.known_to_fail = True
                failed.append(t)
        if failed:
            if alternate := self._find_substitute(exchange, graph, transplants=failed):
                performed, new_failing, new_bridge = self._perform_exchange(
                    alternate, period, graph
                )
                return performed, new_failing + failed, new_bridge
            return None, failed, None
        # if all okay, perform transplants (mark people as transplanted in period)
        for pair in exchange.allPairs():
            if pair[1] is None:  # NDD
                pair[0].status = Status.Transplanted
            else:
                pair[1].status = Status.Transplanted
        # make bridge donor if option allowed and chain
        bridge_donor: Optional[Donor] = None
        if self.allow_bridge_donors and exchange.chain:
            orig_donor = exchange.allDonors()[-1]
            bridge_donor = Donor(f"B_{orig_donor.id}")
            bridge_donor.NDD = True
            bridge_donor.status = Status.InPool
            bridge_donor.bloodGroup = orig_donor.bloodGroup
            try:
                bridge_donor.age = orig_donor.age
            except KEPDataValidationException:
                # Unknown age, which is okay
                pass
            for t in orig_donor.transplants():
                bridge_donor.addTransplant(
                    Transplant(bridge_donor, t.recipient, t.weight)
                )
        return exchange, [], bridge_donor

    def _return_to_pool(
        self,
        exchange: Exchange,
    ) -> None:
        """Return all people in the given exchange to the pool who had been
        selected but not transplanted (due to part or all of the exchange
        failing), ready for selection in a further match run.

        :param exchange: The exchange in question
        """
        for pair in exchange.allPairs():
            if pair[1] is None:
                if pair[0].status == Status.Selected:
                    pair[0].status = Status.InPool
            else:
                if pair[1].status == Status.Selected:
                    pair[1].status = Status.InPool

    def _select_exchange(self, exchange: Exchange) -> int:
        """Mark all transplants as selected in the given exchange.

        :param exchange: The exchange in question.
        """
        for recip in exchange.allRecipients():
            recip.status = Status.Selected
        for donor in exchange.allDonors():
            if donor.NDD:
                donor.status = Status.Selected
        return self.scheduler(exchange)

    def reset(self) -> None:
        """Reset all donors and recipients to have a status of NotYetArrived,
        and ensure we have no known failing transplants."""
        for recipient in self._instance.allRecipients():
            recipient.status = Status.NotYetArrived
        for donor in self._instance.allDonors():
            donor.status = Status.NotYetArrived
        for transplant in self._instance.transplants:
            transplant.known_to_fail = False

    def run(self) -> tuple[
        list[tuple[Instance, Model, Solution]],
        dict[int, list[Exchange]],
    ]:
        """Run the simulation.

        :return: A tuple containing a list of Instance, Model, Solution triples
        (one per matching run performed) as well as a dictionary mapping
        periods to the list of Exchanges performed in that period.
        """
        assigned_exchanges: list[list[tuple[Exchange, int]]] = [
            [] for _ in range(self.periods)
        ]
        graphs: list[CompatibilityGraph] = []
        results: list[tuple[Instance, Model, Solution]] = []
        bridge_donors: list[Donor] = []
        bridge_donor_orig_recip: MutableMapping[str, str]
        exchanges_performed: dict[int, list[Exchange]] = defaultdict(list)
        for period in range(self.periods):
            logger.info(f"Period {period} of {self.periods}")
            bridge_donors = self._handle_arrival_attrition(period, bridge_donors)
            if self.match_run_fn(
                period, self._instance.allRecipients(), self._instance.allDonors()
            ):
                solution, model, instance = self._match_run(
                    period,
                    bridge_donors,
                )
                logger.info(
                    f"Performed match run with {len(instance.allRecipients())} recipients"
                )
                graphs.append(model.graph)
                results.append((instance, model, solution))
                # assign selected exchanges to times based on scheduler
                for modelled in solution.selected:
                    exchange = modelled.exchange
                    delay = self._select_exchange(exchange)
                    while len(assigned_exchanges) <= period + delay:
                        assigned_exchanges.append([])
                    logger.info(
                        f"Assigning {exchange=} to time {period + delay} ({period=} {delay=})"
                    )
                    assigned_exchanges[period + delay].append(
                        (exchange, len(graphs) - 1)
                    )
            for assigned, assigned_run in assigned_exchanges[period]:
                exchanged, new_failures, new_bridge_donor = self._perform_exchange(
                    assigned,
                    period,
                    graphs[assigned_run],
                )
                if exchanged is not None:
                    exchanges_performed[period].append(exchanged)
                if new_bridge_donor:
                    bridge_donors.append(new_bridge_donor)
        for period in range(self.periods, len(assigned_exchanges)):
            logger.info(
                f"Period {period} of {self.periods} (only performing scheduled exchanges)"
            )
            for assigned, assigned_run in assigned_exchanges[period]:
                exchanged, new_failures, new_bridge_donor = self._perform_exchange(
                    assigned,
                    period,
                    graphs[assigned_run],
                )
                if exchanged is not None:
                    exchanges_performed[period].append(exchanged)
                if new_bridge_donor:
                    bridge_donors.append(new_bridge_donor)
        return results, exchanges_performed
