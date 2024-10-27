import unittest
from unittest.mock import patch
from datetime import datetime
from main import *

class TestTaskTracker(unittest.TestCase):
    @patch("main.write_data")
    @patch("main.read_data") 
    def test_add(self, mock_read_data, mock_write_data):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "TODO", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        expected_task_id = "2"
        expected_task_data = {
            "description": "New task",
            "status": "TODO",
            "createdAt": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
            "modifiedAt": str(datetime.now().strftime("%Y-%m-%d %H:%M"))
        }
        add("New task")
        mock_read_data.assert_called_once()
        mock_write_data.assert_called_once_with({
            "1": {"description": "Existing task", "status": "TODO", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"},
            expected_task_id: expected_task_data
        })

    @patch("main.write_data")
    @patch("main.read_data") 
    def test_update(self, mock_read_data, mock_write_data):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        new_desc = "Updated description"
        update("1", new_desc)
        mock_read_data.assert_called_once()
        mock_write_data.assert_called_once_with({
            "1": {"description": new_desc, "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": datetime.now().strftime("%Y-%m-%d %H:%M")}
        })

    @patch("main.read_data") 
    def test_update_doesnt_exist(self, mock_read_data):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        with self.assertRaises(Exception):
            update("3", "new description")

    @patch("main.write_data")
    @patch("main.read_data") 
    def test_mark(self, mock_read_data, mock_write_data):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        mark("1", "in-progress")
        mock_read_data.assert_called_once()
        mock_write_data.assert_called_once_with({
            "1": {"description": "Existing task", "status": "in-progress", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}
        })

    @patch("main.read_data") 
    def test_mark_invalid(self, mock_read_data):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        with self.assertRaises(Exception):
            mark("1", "INVALID")
            
    @patch("builtins.print")
    @patch("main.read_data") 
    def test_list(self, mock_read_data, mock_print):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"},
                                       "2": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        list()
        self.assertEqual(mock_print.call_count, 2)

    @patch("builtins.print")
    @patch("main.read_data") 
    def test_list_todo(self, mock_read_data, mock_print):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "in-progress", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"},
                                       "2": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        list("todo")
        self.assertEqual(mock_print.call_count, 1)
    
    @patch("main.write_data")
    @patch("main.read_data") 
    def test_delete(self, mock_read_data, mock_write_data):
        mock_read_data.return_value = {"1": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"},
                                       "2": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}}        
        delete("1")
        mock_read_data.assert_called_once()
        mock_write_data.assert_called_once_with({
                                       "2": {"description": "Existing task", "status": "todo", "createdAt": "2023-12-31T23:59:59", "modifiedAt": "2023-12-31T23:59:59"}} )       
     
if __name__ == "__main__":
    unittest.main()
