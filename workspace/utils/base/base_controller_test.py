class BaseControllerFlowMock:
    def patch_all_success(self, monkeypatch, step_map: dict, base_path: str):
        """
        將指定函數依序 patch 成靜態成功回傳
        - step_map: {函數名稱: 回傳值}
        - base_path: 例如 "workspace.controller.data_generation_controller"
        """
        for fn_name, return_value in step_map.items():
            monkeypatch.setattr(
                f"{base_path}.{fn_name}",
                self._make_static_return(return_value)
            )

    def patch_fail_on(self, monkeypatch, fail_step: str, fail_code: int, reason: str = "mock_fail", base_path: str = ""):
        """
        將某個函數 patch 成失敗回傳
        - fail_step: 函數名稱，例如 "build_user_data"
        - fail_code: 錯誤碼
        """
        def fail_func(*args, **kwargs):
            return fail_code, None, {"reason": reason}

        monkeypatch.setattr(f"{base_path}.{fail_step}", fail_func)

    def _make_static_return(self, return_value):
        """
        解決 lambda late binding 問題，將每個回傳值綁定成獨立 lambda
        """
        return lambda *args, **kwargs: return_value
