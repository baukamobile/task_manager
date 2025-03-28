import pytest
from tasks.tasks import multiply

@pytest.mark.celery
def test_multiply_task_worker(celery_worker):
    result = muyltiply.delay(2,4)
    assert result.get(timeout=5) == 8