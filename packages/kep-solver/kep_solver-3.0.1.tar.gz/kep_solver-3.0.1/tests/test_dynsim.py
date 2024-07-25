import random
import numpy as np

from kep_solver.entities import Status
from kep_solver.programme import Programme, DynamicSimulation
from kep_solver.fileio import read_file

from kep_solver.model import TransplantCount
from kep_solver.generation import DynamicGenerator

# Seed for RNG for reproducible tests
SEED = 12345


def test_dyn_gen() -> None:
    gen = DynamicGenerator(
        recipient_arrival_rate=100,
        recipient_attrition_function=lambda r: 0,
        recipient_illness_function=lambda r: 0,
        recipient_positive_crossmatch_function=lambda r, d: False,
        ndd_arrival_rate=0,
        ndd_attrition_function=lambda d: 0,
        ndd_illness_function=lambda d: 0,
    )
    instance = read_file("tests/test_instances/test3.json")
    dyn_instance = gen.generate(instance, periods=25)
    assert len(dyn_instance.recipients) == 3
    assert len(dyn_instance.allNDDs()) == 0


def test_with_substitute() -> None:
    programme = Programme(
        [TransplantCount()],
        maxCycleLength=3,
        maxChainLength=3,
        description="Programme",
    )
    gen = DynamicGenerator(
        recipient_arrival_rate=100,
        recipient_attrition_function=lambda r: 0,
        recipient_illness_function=lambda r: r.id == "2" and 1 or 0,
        recipient_positive_crossmatch_function=lambda r, d: False,
        ndd_arrival_rate=0,
        ndd_attrition_function=lambda d: 0,
        ndd_illness_function=lambda d: 0,
    )
    instance = read_file("tests/test_instances/test3.json")
    dyn_instance = gen.generate(instance, periods=25)
    assert len(dyn_instance.allRecipients()) == 3
    assert len(dyn_instance.allNDDs()) == 0
    dynsim = DynamicSimulation(
        programme,
        periods=25,
        dynamic_instance=dyn_instance,
        match_run_fn=lambda period, _, __: period % 4 == 0,
        scheduler=lambda exchange: 1,
        allow_bridge_donors=False,
        recourse="Internal",
    )
    print(dyn_instance.recipient_illnesses)
    results, exchanged = dynsim.run()
    for p, r in enumerate(results):
        instance, model, sol = r
        selected = sum(len(e) for e in sol.selected)
        print(f"At {p=} {instance=} {selected=}")
    # 7 match runs (t \in 0, 4, 8, 12, 16, 20, 24)
    assert len(results) == 7
    our_sol = results[0][2]
    print(our_sol.selected)
    print(our_sol.selected[0].exchange)
    # We selected 1 exchange
    assert len(our_sol.selected) == 1
    # It originally selected a 3-cycle
    assert len(our_sol.selected[0]) == 3
    # But had to fall back to a 2-cycle. Note that this occurs in period 1,
    # while the match run was in period 0 (and
    assert len(exchanged[1]) == 1
    assert len(exchanged[1][0]) == 2
    print(dyn_instance.recipients["2"])
    print(dyn_instance.recipients["2"].status)
    assert dyn_instance.recipients["2"].status == Status.InPool


def test_larger() -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    programme = Programme(
        [TransplantCount()],
        maxCycleLength=3,
        maxChainLength=3,
        description="Programme",
    )
    gen = DynamicGenerator(
        recipient_arrival_rate=3,
        recipient_attrition_function=lambda r: 0.05,
        recipient_illness_function=lambda r: 0,
        recipient_positive_crossmatch_function=lambda r, d: False,
        ndd_arrival_rate=6 / 25,
        ndd_attrition_function=lambda d: 0,
        ndd_illness_function=lambda d: 0,
    )
    instance = read_file("tests/test_instances/medium-3.json")
    dyn_instance = gen.generate(instance, periods=25)
    assert len(dyn_instance.allRecipients()) == 50
    assert len(dyn_instance.allNDDs()) == 6
    dynsim = DynamicSimulation(
        programme,
        periods=25,
        dynamic_instance=dyn_instance,
        match_run_fn=lambda period, _, __: period % 4 == 0,
        scheduler=lambda exchange: int(1 + random.random() * 3),
        allow_bridge_donors=False,
        recourse="Internal",
    )
    results, exchanged = dynsim.run()
    # 7 match runs (t \in 0, 4, 8, 12, 16, 20, 24)
    print(exchanged)
    assert len(results) == 7
    # Look at first match run result
    our_sol = results[0][2]
    # We selected 1 exchange
    assert len(our_sol.selected) == 1
    # It is a 2-chain
    assert len(our_sol.selected[0]) == 2
    assert our_sol.selected[0].exchange.chain == True
    # It is performed in period 2
    assert len(exchanged[2][0]) == 2
    # Check that only the right people have arrived
    assert "28" not in [r.id for r in results[0][0].allRecipients()]
    assert "17" not in [r.id for r in results[0][0].allRecipients()]
    assert "0" in [r.id for r in results[0][0].allRecipients()]
    assert "1" in [r.id for r in results[0][0].allRecipients()]
    assert "19" in [r.id for r in results[0][0].allRecipients()]
    # Check that these right people have arrived for the next match run
    assert "28" in [r.id for r in results[1][0].allRecipients()]
    assert "17" in [r.id for r in results[1][0].allRecipients()]
    # Check that people leave when they claim they will
    assert "32" in [r.id for r in results[-1][0].allRecipients()]
    assert "6" not in [r.id for r in results[-1][0].allRecipients()]
