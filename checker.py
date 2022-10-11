from playwright.sync_api import Playwright, sync_playwright, expect
import time


name_file = "names-sorted.txt"
unavailable_file = "unavailable.txt"
available_file = "available.txt"
mail_suffix = ".zhang"


def do_check(page, name):
    # Fill [aria-label="用户名"]
    page.locator("[aria-label=\"用户名\"]").fill(name)
    # Click img
    page.locator("img").click()
    time.sleep(4)
    # Click text=已有人使用了该用户名，请尝试其他用户名。
    if page.is_visible("text=已有人使用了该用户名，请尝试其他用户名。"):
        return False
    if page.is_visible(
        "section div[role=\"presentation\"] div:has-text(\"您可以使用字母、数字和英文句点\")"):
        return True


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
                   "like Gecko) Chrome/105.0.0.0 Safari/537.36")

    # Open new page
    page = context.new_page()

    # Go to https://accounts.google.com/signup/v2/webcreateaccount?biz=true&cc=JP&continue=https
    # %3A%2F%2Fmyaccount.google.com%2F%3Ftab%3Dkk%26hl%3Dzh_CN&dsh=S-83709954%3A1665454602983084
    # &flowEntry=SignUp&flowName=GlifWebSignIn&hl=zh_CN&service=accountsettings
    page.goto(
        "https://accounts.google.com/signup/v2/webcreateaccount?biz=true&cc=JP&continue=https%3A"
        "%2F%2Fmyaccount.google.com%2F%3Ftab%3Dkk%26hl%3Dzh_CN&dsh=S-83709954%3A1665454602983084"
        "&flowEntry=SignUp&flowName=GlifWebSignIn&hl=zh_CN&service=accountsettings")

    f = open(name_file, "r")
    checked_name = {line.strip() for line in open(unavailable_file, 'r')}
    pass_name = {line.strip() for line in open("available.txt", 'r')}
    unavailable_f = open(unavailable_file, 'a')
    ava_f = open(available_file, 'a')
    for name in f:
        name = name.strip()
        if not name or name == "":
            continue
        if name in checked_name:
            continue
        if name in pass_name:
            continue
        res = do_check(page, name.lower() + mail_suffix)
        if res:
            print('available: ' + name)
            ava_f.write(name + '\n')
        else:
            unavailable_f.write(name + '\n')
    unavailable_f.close()
    f.close()
    ava_f.close()
    context.close()
    browser.close()
    print("done")


with sync_playwright() as playwright:
    run(playwright)
