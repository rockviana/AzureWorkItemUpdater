from azure_devops_updater import AzureDevOpsUpdater

pat_token = 'YOUR_PAT_TOKEN'
organization_url = 'https://dev.azure.com/YOUR_ORG'
project_name = 'YOUR_PROJECT_NAME'
updated_work_item_id = 2907

updater = AzureDevOpsUpdater(organization_url, pat_token, project_name)
updater.update_tree_from_work_item(updated_work_item_id)
