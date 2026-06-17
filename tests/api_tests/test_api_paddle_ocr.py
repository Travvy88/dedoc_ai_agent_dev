import json
import os
import unittest

from tests.api_tests.abstract_api_test import AbstractTestApiDocReader

class TestApiPaddleOCR(AbstractTestApiDocReader):

    def _get_abs_path(self, file_name: str) -> str:
        return os.path.join(self.data_directory_path, "scanned", file_name)

    def _get_tree_text(self, tree: dict) -> str:
        texts = []
        stack = [tree]
        while stack:
            node = stack.pop()
            texts.append(node.get("text", ""))
            stack.extend(node.get("subparagraphs", []))
        return " ".join(texts)

    def _check_successful_response(self, result: dict, file_name: str, check_tree_has_text: bool = True) -> dict:
        self.assertIn("content", result)
        tree = result["content"]["structure"]
        self._check_tree_sanity(tree)
        self.assertIn("metadata", result)
        self.assertEqual(result["metadata"]["file_name"], file_name)

        if check_tree_has_text:
            all_text = self._get_tree_text(tree)
            self.assertGreater(len(all_text.strip()), 0, f"Empty text tree for {file_name}")

        return tree

    def test_paddle_v5_russian_scanned_pdf(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v5_server", language="rus", pdf_with_text_layer="false"
        ))
        tree = self._check_successful_response(result, file_name)
        all_text = self._get_tree_text(tree)
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("Пример документа", node["text"].strip().split("\n")[0])
        self.assertIn("одну строчку.", all_text)
        self.assertIn("Какие то определения", all_text)
        self.assertIn("Дадим пояснения", all_text)

    
    def test_paddle_v6_english_scanned_image(self) -> None:
        file_name = "example.bmp"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v6_medium", language="eng"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        all_text = self._get_tree_text(tree)
        self.assertGreaterEqual(len(tree.get("subparagraphs", [])), 3,
            f"Expected >= 4 top-level nodes in tree, got {len(tree.get('subparagraphs', []))}")
        self.assertIn("1.2.1", all_text)
        self.assertIn("1.2.2", all_text)
        self.assertIn("1.2.3", all_text)

    
    def test_paddle_v5_dual_language(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v5_server", language="rus+eng", pdf_with_text_layer="false"
        ))
        tree = self._check_successful_response(result, file_name)
        all_text = self._get_tree_text(tree)
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("Пример документа", node["text"].strip().split("\n")[0])
        self.assertIn("одну строчку.", all_text)
        self.assertIn("Какие то определения", all_text)
        self.assertIn("Дадим пояснения", all_text)

    
    def test_paddle_v5_server_model(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v5_server", language="rus", pdf_with_text_layer="false"
        ))
        tree = self._check_successful_response(result, file_name)
        all_text = self._get_tree_text(tree)
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("Пример документа", node["text"].strip().split("\n")[0])
        self.assertIn("одну строчку.", all_text)
        self.assertIn("Какие то определения", all_text)
        self.assertIn("Дадим пояснения", all_text)

    
    def test_paddle_v6_small_model(self) -> None:
        file_name = "example.bmp"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v6_small", language="eng"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        all_text = self._get_tree_text(tree)
        self.assertGreaterEqual(len(tree.get("subparagraphs", [])), 3,
            f"Expected >= 4 top-level nodes in tree, got {len(tree.get('subparagraphs', []))}")
        self.assertIn("1.2.1", all_text)
        self.assertIn("1.2.2", all_text)
        self.assertIn("1.2.3", all_text)

    
    def test_paddle_v6_tiny_model(self) -> None:
        file_name = "example.bmp"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v6_tiny", language="eng"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        all_text = self._get_tree_text(tree)
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("∏péMep AokyMeHra", node["text"].strip().split("\n")[0])
        self.assertIn("ΓIaBa 1", all_text)
        self.assertIn("OAHy CTpO4Ky", all_text)
        self.assertIn("1.2.1", all_text)
        self.assertIn("1.2.2", all_text)
        self.assertIn("1.2.3", all_text)

    
    def test_paddle_v6_short_language_notation(self) -> None:
        file_name = "example.bmp"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v6_medium", language="en"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        all_text = self._get_tree_text(tree)
        self.assertGreaterEqual(len(tree.get("subparagraphs", [])), 3,
            f"Expected >= 4 top-level nodes in tree, got {len(tree.get('subparagraphs', []))}")
        self.assertIn("1.2.1", all_text)
        self.assertIn("1.2.2", all_text)
        self.assertIn("1.2.3", all_text)

    
    def test_paddle_v5_short_language_notation(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v5_server", language="ru", pdf_with_text_layer="false"
        ))
        tree = self._check_successful_response(result, file_name)
        all_text = self._get_tree_text(tree)
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("Пример документа", node["text"].strip().split("\n")[0])
        self.assertIn("одну строчку.", all_text)
        self.assertIn("Какие то определения", all_text)
        self.assertIn("Дадим пояснения", all_text)

    def test_tesseract_default_unchanged(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(
            ocr_engine="tesseract", language="rus", pdf_with_text_layer="false",
            need_pdf_table_analysis="false"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("Пример документа", node["text"].strip().split("\n")[0])
        all_text = self._get_tree_text(tree)
        self.assertIn("одну строчку.", all_text)
        self.assertIn("Какие то определения", all_text)
        self.assertIn("Дадим пояснения", all_text)
        self.assertIn("Глава 1", all_text)

    
    def test_paddleocr_with_attachments_false(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v5_server", language="rus", with_attachments="false", pdf_with_text_layer="false"
        ))
        tree = self._check_successful_response(result, file_name)
        all_text = self._get_tree_text(tree)
        node = self._get_by_tree_path(tree, "0.0")
        self._check_similarity("Пример документа", node["text"].strip().split("\n")[0])
        self.assertIn("одну строчку.", all_text)
        self.assertIn("Какие то определения", all_text)
        self.assertIn("Дадим пояснения", all_text)
        self.assertEqual([], result.get("attachments", []))

    
    def test_paddle_v6_german(self) -> None:
        file_name = "example.bmp"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v6_medium", language="de"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        all_text = self._get_tree_text(tree)
        self.assertGreaterEqual(len(tree.get("subparagraphs", [])), 3,
            f"Expected >= 4 top-level nodes in tree, got {len(tree.get('subparagraphs', []))}")
        self.assertIn("1.2.1", all_text)
        self.assertIn("1.2.2", all_text)
        self.assertIn("1.2.3", all_text)

    def test_paddle_v5_error_v6_cyrillic(self) -> None:
        file_name = "example.pdf"
        error_response = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v6_medium", language="rus", pdf_with_text_layer="false"
        ), expected_code=400)
        self.assertIn("message", error_response)
        error_msg = error_response["message"] if isinstance(error_response, dict) else error_response
        self.assertIn("not supported", error_msg)
        self.assertIn("PP-OCRv6", error_msg)

    
    def test_paddle_v5_multiple_scanned_images(self) -> None:
        file_name = "example.pgm"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v5_server", language="eng"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        all_text = self._get_tree_text(tree)
        self.assertGreaterEqual(len(tree.get("subparagraphs", [])), 3,
            f"Expected >= 4 top-level nodes, got {len(tree.get('subparagraphs', []))}")
        self.assertIn("1.2.1", all_text)
        self.assertIn("1.2.2", all_text)
        self.assertIn("1.2.3", all_text)

    
    def test_paddle_v6_with_table_analysis(self) -> None:
        file_name = "example.pdf"
        result = self._send_request(file_name, data=dict(
            ocr_engine="paddle_v6_medium", language="eng", need_pdf_table_analysis="true", pdf_with_text_layer="false"
        ))
        self._check_successful_response(result, file_name)
        tree = result["content"]["structure"]
        all_text = self._get_tree_text(tree)
        self.assertIn("1.2.1", all_text)
        self.assertIn("1.2.2", all_text)
        self.assertIn("1.2.3", all_text)
        tables = result["content"].get("tables", [])
        self.assertIsInstance(tables, list)
