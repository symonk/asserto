import pytest

NO_UNTRIGGERED_WARNINGS = pytest.mark.filterwarnings("ignore::asserto._warnings.NoAssertAttemptedWarning")
