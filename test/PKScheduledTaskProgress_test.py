import unittest
from unittest.mock import MagicMock

from pkscreener.classes.PKScheduledTaskProgress import PKScheduledTaskProgress

class TestPKScheduledTaskProgress(unittest.TestCase):
    
    def setUp(self):
        self.task_progress = PKScheduledTaskProgress()
        # Mocking a task object
        self.mock_task = MagicMock()
        self.mock_task.progress = 50
        self.mock_task.total = 100
        self.mock_task.progressStatusDict = {}
        
        # Adding a mock task to the task dictionary
        self.task_progress.tasksDict['task1'] = self.mock_task

    def test_update_progress_valid_task(self):
        """ Test updating progress for a valid task ID. """
        self.task_progress.updateProgress('task1')
        self.assertIn('task1', self.mock_task.progressStatusDict)
        self.assertEqual(self.mock_task.progressStatusDict['task1'], {"progress": 50, "total": 100})

    def test_update_progress_invalid_task(self):
        """ Test updating progress for an invalid task ID. """
        initial_length = len(self.mock_task.progressStatusDict)
        self.task_progress.updateProgress('invalid_task_id')
        self.assertEqual(len(self.mock_task.progressStatusDict), initial_length)
        
    def test_update_progress_no_task(self):
        """ Test updating progress when no task is present. """
        self.task_progress.tasksDict.clear()  # Clear all tasks
        initial_length = len(self.mock_task.progressStatusDict)
        self.task_progress.updateProgress('task1')
        self.assertEqual(len(self.mock_task.progressStatusDict), initial_length)

    def test_progress_updater_called(self):
        """ Test that progressUpdater.refresh is called when task is valid. """
        from pkscreener.classes import PKScheduler
        PKScheduler.progressUpdater = MagicMock()
        self.task_progress.updateProgress('task1')
        PKScheduler.progressUpdater.refresh.assert_called_once()

    def test_progress_updater_not_called(self):
        """ Test that progressUpdater.refresh is not called when task is invalid. """
        global progressUpdater
        progressUpdater = MagicMock()
        self.task_progress.updateProgress('invalid_task_id')
        progressUpdater.refresh.assert_not_called()
