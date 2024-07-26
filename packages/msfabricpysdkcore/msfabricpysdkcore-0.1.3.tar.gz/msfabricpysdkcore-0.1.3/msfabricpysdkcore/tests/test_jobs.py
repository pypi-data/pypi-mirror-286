import unittest
from msfabricpysdkcore.coreapi import FabricClientCore
from dotenv import load_dotenv

load_dotenv()


class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        #load_dotenv()
        self.fc = FabricClientCore()
        self.workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'
        self.item_id = "38a1c15f-8a9e-49c5-8d05-a27cf9ce8b18"


    def test_jobs_end_to_end(self):
        job = self.fc.run_on_demand_item_job(workspace_id=self.workspace_id,
                                            item_id=self.item_id,
                                            job_type="RunNotebook")
        
        self.assertEqual(job.item_id, self.item_id)
        self.assertEqual(job.workspace_id, self.workspace_id)
        self.assertEqual(job.job_type, "RunNotebook")
        self.assertIn(job.status, ["NotStarted", "InProgress"])
        self.assertEqual(job.invoke_type, "Manual")

        job2 = self.fc.get_item_job_instance(workspace_id=self.workspace_id,
                                        item_id=self.item_id,
                                        job_instance_id=job.id)
        
        self.assertEqual(job.id, job2.id)

        status_code = self.fc.cancel_item_job_instance(workspace_id=self.workspace_id,
                                                  item_id=self.item_id,
                                                  job_instance_id=job.id)

        self.assertEqual(status_code, 202)

if __name__ == "__main__":
    unittest.main()

