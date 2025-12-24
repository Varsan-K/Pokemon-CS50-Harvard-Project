#Copy of code from original

from project import compute_target, gyms_milestones, update_progress

def test_compute_target():
    expenses = {"needs": 50000.0, "wants": 30000.0, "savings": 20000.0}
    yearly_income = 100000
    targets = compute_target(expenses, yearly_income)
    assert targets["targets"]["needs"] == 50000.0
    assert targets["targets"]["wants"] == 30000.0
    assert targets["targets"]["savings"] == 20000.0

    expenses = {"needs": 30000.0, "wants": 10000.0, "savings": 15000.0}
    yearly_income = 100000
    deltatest = compute_target(expenses, yearly_income)
    assert deltatest["deltas"]["needs"] == 20000.0
    assert deltatest["deltas"]["wants"] == 20000.0
    assert deltatest["deltas"]["savings"] == 5000.0

def test_gyms_milestones():
    total_saved = 200
    milestones = [300, 200, 400]
    assert gyms_milestones(total_saved, milestones) == 1
    total_saved = 1000
    milestones = [500, 200, 300]

    assert gyms_milestones(total_saved, milestones) == 3
    total_saved = 50
    milestones = [500, 200, 300]
    assert gyms_milestones(total_saved, milestones) == 0

def test_update_progress():
    milestones = [200,300,500]
    total_saved = 200
    progress = update_progress(total_saved, milestones)
    assert progress["level"] == 2
    assert progress["stage"] == 1
    assert progress["xp"] == 0.0

    milestones = [200,300,400,500,600,700]
    total_saved = 350
    progress = update_progress(total_saved, milestones)
    assert progress["level"] == 3
    assert progress["stage"] == 1
    assert progress["xp"] == 50.0

    milestones = []
    total_saved = 50
    progress = update_progress(total_saved, milestones)
    assert progress["level"] == 1
    assert progress["stage"] == 1
    assert progress["xp"] == 0.0

    milestones = [200,300,500]
    total_saved = 250
    progress = update_progress(total_saved, milestones)
    assert progress["level"] == 2
    assert progress["stage"] == 1
    assert progress["xp"] == 50.0

    milestones = [1000,2000,3000]
    total_saved = 4000
    progress = update_progress(total_saved, milestones)
    assert progress["level"] == 4
    assert progress["stage"] == 3
    assert progress["xp"] == 100.0

    milestones = [1000,2000,3000]
    total_saved = 3000
    progress = update_progress(total_saved, milestones)
    assert progress["level"] == 4
    assert progress["stage"] == 3
    assert progress["xp"] == 100.0
