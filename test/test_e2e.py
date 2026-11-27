import os
import json
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

# 在 Docker Compose 內部網路中，直接透過服務名稱 "web" 連線
BASE_URL = os.getenv("BASE_URL", "http://web")
REPORT_DIR = "/app/reports"


def run_e2e_tests():
    os.makedirs(REPORT_DIR, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    steps_log = []

    print(f"🎭 開始執行全端 E2E 自動化測試，目標站台：{BASE_URL}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 在 Docker 環境中，headless 模式可能需要額外設定，這裡先設為 False 方便除錯
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        try:
            # --------------------------------------------------
            # 步驟 1：開啟首頁並驗證標題載入 (GET)
            # --------------------------------------------------
            page.goto(BASE_URL, wait_until="networkidle", timeout=15000)
            expect(page.locator("h1")).to_contain_text("全端消費記帳管理系統")
            steps_log.append({"step": "1_load_homepage", "status": "PASS"})
            print("✅ [1/4] 首頁載入與標題驗證通過")

            # --------------------------------------------------
            # 步驟 2：填寫表單新增一筆消費紀錄 (POST)
            # --------------------------------------------------
            test_item_name = f"E2E測試_機械鍵盤_{run_id[-4:]}"
            page.fill("#input-name", test_item_name)
            page.fill("#input-amount", "3500")
            page.select_option("#input-category", "3C周邊")
            page.click("#btn-submit")

            # 定位剛剛新增的那一列資料並驗證金額顯示為 $3500
            target_row = page.locator("tr", has_text=test_item_name)
            expect(target_row).to_be_visible(timeout=5000)
            expect(target_row.locator(".item-amount")).to_have_text("$3500")

            shot_create = f"e2e_{run_id}_1_created.png"
            page.screenshot(path=os.path.join(REPORT_DIR, shot_create), full_page=True)
            steps_log.append({"step": "2_create_item_POST", "status": "PASS", "screenshot": shot_create})
            print(f"✅ [2/4] 新增項目驗證通過：{test_item_name} ($3500)")

            # --------------------------------------------------
            # 步驟 3：行內編輯修改金額並重新整理驗證持久化 (PUT + DB)
            # --------------------------------------------------
            target_row.locator(".btn-edit").click()
            target_row.locator(".edit-amount").fill("3200")
            target_row.locator(".btn-save").click()

            # 驗證畫面即時更新為 $3200
            expect(target_row.locator(".item-amount")).to_have_text("$3200", timeout=5000)

            # 重新整理頁面（F5），確保資料真的寫入 PostgreSQL 而非僅前端假象
            page.reload(wait_until="networkidle")
            reloaded_row = page.locator("tr", has_text=test_item_name)
            expect(reloaded_row.locator(".item-amount")).to_have_text("$3200")

            shot_update = f"e2e_{run_id}_2_updated.png"
            page.screenshot(path=os.path.join(REPORT_DIR, shot_update), full_page=True)
            steps_log.append({"step": "3_update_item_PUT_and_reload", "status": "PASS", "screenshot": shot_update})
            print("✅ [3/4] 修改金額 ($3200) 與重新整理資料庫持久化驗證通過")

            # --------------------------------------------------
            # 步驟 4：刪除測試資料並確認從畫面消失 (DELETE)
            # --------------------------------------------------
            reloaded_row.locator(".btn-del").click()
            expect(page.locator("tr", has_text=test_item_name)).to_have_count(0, timeout=5000)

            shot_delete = f"e2e_{run_id}_3_deleted.png"
            page.screenshot(path=os.path.join(REPORT_DIR, shot_delete), full_page=True)
            steps_log.append({"step": "4_delete_item_DELETE", "status": "PASS", "screenshot": shot_delete})
            print("✅ [4/4] 刪除項目驗證通過，測試資料已清理完畢")

            overall_status = "PASS"

        except Exception as e:
            err_shot = f"e2e_{run_id}_ERROR.png"
            page.screenshot(path=os.path.join(REPORT_DIR, err_shot), full_page=True)
            steps_log.append({"step": "error_captured", "status": "FAIL", "error": str(e), "screenshot": err_shot})
            overall_status = "FAIL"
            print(f"❌ E2E 測試失敗：{e}")
            raise
        finally:
            browser.close()
            report_file = os.path.join(REPORT_DIR, f"e2e_report_{run_id}.json")
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "overall_status": overall_status,
                        "target_url": BASE_URL,
                        "executed_at": datetime.now().isoformat(),
                        "steps": steps_log,
                    },
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            print(f"📄 測試報告已匯出至：{report_file}")


if __name__ == "__main__":
    run_e2e_tests()