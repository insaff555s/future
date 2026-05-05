import unittest
import json, os
from main import App

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.win.withdraw()
    
    def test_add_task_valid(self):
        self.app.entry_task.insert(0, "Тест")
        self.app.entry_type.insert(0, "работа")
        self.app.add_task()
        self.assertTrue(any(t["task"] == "Тест" for t in self.app.tasks))
    
    def test_add_task_empty(self):
        initial_count = len(self.app.tasks)
        self.app.entry_task.insert(0, "")
        self.app.entry_type.insert(0, "")
        self.app.add_task()
        self.assertEqual(len(self.app.tasks), initial_count)
    
    def test_generate_with_filter(self):
        self.app.filter.set("учёба")
        self.app.generate()
        self.assertTrue(len(self.app.history) > 0)
        self.assertEqual(self.app.history[-1]["type"], "учёба")
    
    def test_json_save_load(self):
        test_data = [{"task": "test", "type": "тест", "time": "01.01.2024 00:00"}]
        self.app.save_json("test.json", test_data)
        loaded = self.app.load_json("test.json")
        self.assertEqual(loaded, test_data)
        os.remove("test.json")
    
    def tearDown(self):
        self.app.win.destroy()

if name == "__main__":
    unittest.main()