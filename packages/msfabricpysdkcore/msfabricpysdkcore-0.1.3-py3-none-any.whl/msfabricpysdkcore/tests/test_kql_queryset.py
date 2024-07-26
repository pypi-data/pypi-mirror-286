import unittest
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
from msfabricpysdkcore.coreapi import FabricClientCore

load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        #load_dotenv()
        self.fc = FabricClientCore()

        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.item_name = "testitem" + datetime_str
        self.item_type = "Notebook"
    
    def test_kql_querysets(self):

        fc = self.fc
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'

        kql_queryset_name = "kqlqueryset1"

        kql_querysets = fc.list_kql_querysets(workspace_id)
        kql_queryset_names = [kqlq.display_name for kqlq in kql_querysets]
        self.assertGreater(len(kql_querysets), 0)
        self.assertIn(kql_queryset_name, kql_queryset_names)

        kqlq = fc.get_kql_queryset(workspace_id, kql_queryset_name=kql_queryset_name)
        self.assertIsNotNone(kqlq.id)
        self.assertEqual(kqlq.display_name, kql_queryset_name)

        kqlq2 = fc.update_kql_queryset(workspace_id, kqlq.id, display_name=f"{kql_queryset_name}2", return_item=True)

        kqlq = fc.get_kql_queryset(workspace_id, kql_queryset_id=kqlq.id)
        self.assertEqual(kqlq.display_name, f"{kql_queryset_name}2")
        self.assertEqual(kqlq.id, kqlq2.id)

        kqlq2 = fc.update_kql_queryset(workspace_id, kqlq.id, display_name=kql_queryset_name, return_item=True)

        kqlq = fc.get_kql_queryset(workspace_id, kql_queryset_id=kqlq.id)
        self.assertEqual(kqlq.display_name, kql_queryset_name)
        self.assertEqual(kqlq.id, kqlq2.id)

        # status_code = fc.delete_kql_queryset(workspace_id, kqlq.id)
        # self.assertEqual(status_code, 200)