from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class AzureDevOpsUpdater:
    def __init__(self, organization_url, pat_token, project_name, debug=False):
        self.organization_url = organization_url
        self.project_name = project_name
        self.credentials = BasicAuthentication('', pat_token)
        self.connection = Connection(base_url=organization_url, creds=self.credentials)
        self.client = self.connection.clients.get_work_item_tracking_client()
        self.debug = debug

    def log(self, message):
        if self.debug:
            print(message)

    def get_work_item(self, work_item_id):
        self.log(f'Retrieving work item {work_item_id}')
        return self.client.get_work_item(work_item_id, expand='all')

    def update_work_item(self, work_item_id, field_name, value):
        patch_document = [{
            'op': 'add',
            'path': f'/fields/{field_name}',
            'value': value
        }]
        self.log(f'Updating work item {work_item_id} with {field_name}={value}')
        self.client.update_work_item(document=patch_document, id=work_item_id)

    def sum_sibling_effort(self, parent_work_item_id):
        self.log(f'Summing sibling efforts for parent work item {parent_work_item_id}')
        parent_work_item = self.get_work_item(parent_work_item_id)
        if not parent_work_item or not hasattr(parent_work_item, 'relations') or not parent_work_item.relations:
            self.log(f'No relations found for work item {parent_work_item_id}')
            return 0

        total_effort = 0
        for relation in parent_work_item.relations:
            if relation.rel == 'System.LinkTypes.Hierarchy-Forward':
                child_id = int(relation.url.split('/')[-1])
                self.log(f'Found child work item {child_id} for parent {parent_work_item_id}')
                child_work_item = self.get_work_item(child_id)
                child_effort = child_work_item.fields.get('Custom.ExpectedEffort', 0)
                self.log(f'Child work item {child_id} has effort {child_effort}')
                total_effort += child_effort

        self.log(f'Total sibling effort for parent work item {parent_work_item_id} is {total_effort}')
        return total_effort

    def update_parent_effort(self, work_item_id):
        self.log(f'Updating parent effort for work item {work_item_id}')
        work_item = self.get_work_item(work_item_id)
        parent_id = None
        for relation in work_item.relations:
            if relation.rel == 'System.LinkTypes.Hierarchy-Reverse':
                parent_id = int(relation.url.split('/')[-1])
                self.log(f'Found parent work item {parent_id} for work item {work_item_id}')
                break

        if parent_id:
            total_effort = self.sum_sibling_effort(parent_id)
            self.update_work_item(parent_id, 'Custom.ExpectedEffort', total_effort)
            self.update_parent_effort(parent_id)
        else:
            self.log(f'No parent found for work item {work_item_id}')

    def update_tree_from_work_item(self, work_item_id):
        self.log(f'Updating tree starting from work item {work_item_id}')
        self.update_parent_effort(work_item_id)