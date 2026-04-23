from PACKAGE_NAME.training.callbacks import EarlyStopping


def test_counter_resets_on_improvement():
    es = EarlyStopping(patience=3, min_delta=0.01)
    es(1.0)
    es(0.5)
    assert es.counter == 0
    assert not es.early_stop


def test_triggers_after_patience():
    es = EarlyStopping(patience=2, min_delta=0.0)
    es(1.0)
    assert not es.early_stop
    es(1.0)
    es(1.0)
    assert es.early_stop


def test_min_delta_is_respected():
    es = EarlyStopping(patience=2, min_delta=0.5)
    es(1.0)
    es(0.6)
    assert es.counter == 1
    es(0.55)
    assert es.counter == 2
    assert es.early_stop


def test_sub_delta_improvement_does_not_reset():
    es = EarlyStopping(patience=1, min_delta=0.1)
    es(1.0)
    es(0.95)
    assert es.early_stop
