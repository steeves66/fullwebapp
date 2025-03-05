from django.test.runner import DiscoverRunner

class FillData:
    def setup_databases(self, *args, **kwargs):
        print("### populating Test Cases Database ###")
        # Create any data
        print("### Database populated ########")
        return temp
    

class CustomRunner(FillData, DiscoverRunner):
    pass
