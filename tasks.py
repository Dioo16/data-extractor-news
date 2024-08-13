from robocorp.tasks import task
from robocorp import workitems
from main import main
@task
def extract_news_from_website():
    item = workitems.inputs.current
    phrase = item.payload.get("phrase")
    categorys = item.payload.get("categories")
    month = item.payload.get("month")
    main(phrase, categorys, month)