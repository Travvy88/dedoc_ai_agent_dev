.. _configure_ocr_engine:

Configuring the OCR Engine in Dedoc
====================================

Dedoc supports multiple OCR backends for text recognition in image-based PDF
documents and scanned images. This tutorial explains all available OCR
configuration options and how to choose the right engine for your data.

Overview of available engines
-----------------------------

Dedoc provides three OCR engines that can be selected at runtime:

* **Tesseract** (``tesseract``) — the default engine, uses ``pytesseract``.
  Recommended for general-purpose OCR with broad language support via
  system-installed Tesseract language packages. Best when you need many
  languages with simple setup.

* **PP-OCRv5** (``paddle_v5``) — PaddleOCR version 5. Supports **80+ languages**
  including Cyrillic (Russian, Ukrainian, Belarusian), Arabic, Devanagari
  (Hindi), Korean, Thai, Greek, Telugu, Tamil, and all Latin scripts. Language-
  specific recognition models are auto-selected by language group. Use this
  when you need **Cyrillic, Arabic, or wide non-Latin support**.

* **PP-OCRv6** (``paddle_v6``) — PaddleOCR version 6. Supports **50 languages**
  (Latin + Chinese + Japanese). A single multilingual model achieves state-of-
  the-art accuracy and is approximately **5× faster** than v5 on CPU. Use this
  when your documents use only Latin scripts or CJK.

Choosing the right engine:

.. flat-table:: Engine selection guide
    :widths: 15 30 30 25
    :header-rows: 1

    * - Use case
      - Recommended engine
      - Language examples
      - Notes
    * - Russian / Cyrillic documents
      - ``paddle_v5``
      - ``rus``, ``bel``, ``ukr``, ``bul``, ``kaz``
      - v6 does **not** support Cyrillic
    * - English / Western European
      - ``paddle_v6`` or ``tesseract``
      - ``eng``, ``deu``, ``fra``, ``spa``, ``ita``
      - v6 is fastest, tesseract is lightweight
    * - Chinese, Japanese
      - ``paddle_v6``
      - ``chi_sim``, ``chi_tra``, ``jpn``
      - v6 has native CJK support
    * - Arabic, Hindi, Korean, Thai
      - ``paddle_v5``
      - ``ara``, ``hin``, ``kor``, ``tha``
      - v5 has dedicated rec models
    * - Multi-language (mixed scripts)
      - ``paddle_v5``
      - ``rus+eng``, ``ara+eng``
      - Multi-pass OCR merges results
    * - General purpose, simple setup
      - ``tesseract``
      - Any
      - Requires system tessdata packages

.. note::
   PP-OCRv5 and PP-OCRv6 download their models automatically on first
   inference. No manual model installation is required. Tesseract requires
   the appropriate language packages to be installed on the system (see
   :ref:`install_tesseract`).

Language parameter — dual notation
-----------------------------------

The ``language`` parameter accepts both **Tesseract** (3-4 letter) and
**PaddleOCR** (short) language codes. The language mapper
(:class:`~dedoc.readers.pdf_reader.pdf_image_reader.ocr.paddleocr_language_mapper.PaddleOCRLanguageMapper`)
automatically converts between formats:

.. flat-table:: Language code examples
    :widths: 10 25 25 40
    :header-rows: 1

    * - Language
      - Tesseract code
      - PaddleOCR short code
      - Notes
    * - Russian
      - ``rus``
      - ``ru``
      - Both formats work identically
    * - English
      - ``eng``
      - ``en``
      -
    * - German
      - ``deu``
      - ``de``
      -
    * - French
      - ``fra``
      - ``fr``
      -
    * - Russian + English (multi)
      - ``rus+eng``
      - ``ru+en``
      - Mixing formats is allowed

When you pass ``language="rus"`` to a PaddleOCR engine, the mapper
transparently converts it to ``ru`` before inference. Existing Tesseract-format
API calls continue to work without changes.

Engine parameter — ``ocr_engine``
----------------------------------

Choose the OCR backend with the ``ocr_engine`` parameter:

* ``tesseract`` — Tesseract OCR (default). Uses ``pytesseract`` to call the
  system Tesseract installation. Language support depends on installed
  ``tessdata`` packages.

* ``paddle_v6_medium`` — PP-OCRv6 medium model. **50 languages** (Latin + CJK),
  ~133 MB total model size, 86.2% Hmean detection accuracy. Best accuracy
  for Latin scripts and CJK. Does **not** support Cyrillic, Arabic, Devanagari,
  Korean, Thai, or Greek.

* ``paddle_v6_small`` — PP-OCRv6 small model. **50 languages** (Latin + CJK),
  ~30 MB total model size, 84.1% Hmean detection accuracy. Balanced speed
  and accuracy for Latin scripts and CJK.

* ``paddle_v6_tiny`` — PP-OCRv6 tiny model. **50 languages** (Latin + CJK),
  ~6 MB total model size, 80.6% Hmean detection accuracy. Fastest inference,
  minimal memory footprint.

* ``paddle_v5_server`` — PP-OCRv5 server model. **80+ languages**, separate
  recognition models per language group (cyrillic, arabic, devanagari, korean,
  thai, etc.), ~84 MB detection model. Recommended for Cyrillic and Arabic
  scripts.

* ``paddle_v5_mobile`` — PP-OCRv5 mobile model. **80+ languages**, separate
  recognition models per language group, ~5 MB detection model. Lighter and
  faster than server, suitable for resource-constrained environments.



Device parameter — ``device``
------------------------------

Control where OCR inference runs:

* ``cpu`` — Run on CPU (default). Works everywhere, no special hardware
  required. You can configure the number of CPU threads with the
  ``ocr_cpu_threads`` config parameter (default: 10).

* ``gpu:0`` — Run on GPU (CUDA). Requires NVIDIA GPU with ``paddlepaddle-gpu``
  installed. Use ``ocr_precision=fp16`` for additional speedup and
  ``ocr_use_tensorrt=True`` for TensorRT acceleration.

Configuring via ``config.py``
-----------------------------

All OCR parameters can be set globally in the application configuration
dictionary (``dedoc/config.py``):

.. code-block:: python

    config = {
        "ocr_engine": "paddle_v6_medium",
        "ocr_device": "cpu",
        "ocr_precision": "fp32",
        "ocr_use_tensorrt": False,
        "ocr_cpu_threads": 10,
        "ocr_conf_threshold": 0.0,
    }
    manager = DedocManager.from_config(config=config)

Per-request configuration via API
---------------------------------

When using dedoc as a web service, OCR parameters can be set on each request.
Below are curl examples for common scenarios.

**Russian document with PP-OCRv5 (recommended for Cyrillic):**

.. code-block:: bash

    curl -X POST http://localhost:1231/upload \\
        -F "file=@document.pdf" \\
        -F "ocr_engine=paddle_v5_server" \\
        -F "language=rus" \\
        -F "pdf_with_text_layer=false"

**English document with PP-OCRv6 (fastest for Latin scripts):**

.. code-block:: bash

    curl -X POST http://localhost:1231/upload \\
        -F "file=@document.pdf" \\
        -F "ocr_engine=paddle_v6_medium" \\
        -F "language=eng" \
        -F "pdf_with_text_layer=false"

**English document with PP-OCRv6 on GPU:**

.. code-block:: bash

    curl -X POST http://localhost:1231/upload \\
        -F "file=@document.pdf" \\
        -F "ocr_engine=paddle_v6_medium" \\
        -F "device=gpu:0" \\
        -F "language=eng" \\
        -F "pdf_with_text_layer=false"

**Multi-language document (Russian + English) with PP-OCRv5:**

.. code-block:: bash

    curl -X POST http://localhost:1231/upload \\
        -F "file=@document.pdf" \\
        -F "ocr_engine=paddle_v5_server" \\
        -F "language=rus+eng" \\
        -F "pdf_with_text_layer=false"

**Tiny model for maximum speed (PP-OCRv6):**

.. code-block:: bash

    curl -X POST http://localhost:1231/upload \\
        -F "file=@document.pdf" \\
        -F "ocr_engine=paddle_v6_medium" \\
        -F "language=eng" \\
        -F "pdf_with_text_layer=false"

**Tesseract with German language (requires system tessdata):**

.. code-block:: bash

    curl -X POST http://localhost:1231/upload \\
        -F "file=@document.pdf" \\
        -F "ocr_engine=tesseract" \\
        -F "language=deu" \\
        -F "pdf_with_text_layer=false"

Language support summary
------------------------

PP-OCRv6 — **50 languages** (Latin + CJK):

* 4 core languages: English (``en``), Chinese simplified (``ch``), Chinese
  traditional (``chinese_cht``), Japanese (``japan``)
* 46 Latin-script languages: ``af``, ``az``, ``bs``, ``ca``, ``cs``, ``cy``,
  ``da``, ``de``, ``es``, ``et``, ``eu``, ``fi``, ``fr``, ``ga``, ``gl``,
  ``hr``, ``hu``, ``id``, ``is``, ``it``, ``ku``, ``la``, ``lb``, ``lt``,
  ``lv``, ``mi``, ``ms``, ``mt``, ``nl``, ``no``, ``oc``, ``pl``, ``pt``,
  ``qu``, ``rm``, ``ro``, ``rs_latin``, ``sk``, ``sl``, ``sq``, ``sv``,
  ``sw``, ``tl``, ``tr``, ``uz``, ``vi``

PP-OCRv5 — **80+ languages** including:

* **Cyrillic (29 languages):** Russian (``ru``), Belarusian (``be``),
  Ukrainian (``uk``), Bulgarian (``bg``), Mongolian (``mn``), Kazakh (``kk``),
  Kyrgyz (``ky``), Tajik (``tg``), Macedonian (``mk``), Tatar (``tt``),
  Chuvash (``cv``), Bashkir (``ba``), and more
* **Arabic (8 languages):** Arabic (``ar``), Persian (``fa``), Uyghur (``ug``),
  Urdu (``ur``), Pashto (``ps``), Kurdish (``ku``), Sindhi (``sd``),
  Balochi (``bal``)
* **Devanagari (13 languages):** Hindi (``hi``), Marathi (``mr``), Nepali
  (``ne``), Bhojpuri (``bho``), and more
* **Latin (all European languages):** English, German, French, Spanish, Italian,
  Portuguese, Polish, Dutch, Swedish, Danish, Norwegian, Finnish, Czech,
  Hungarian, Romanian, Turkish, Vietnamese, Indonesian, Malay, and more
* **Asian scripts:** Korean (``ko``, ``korean``), Thai (``th``), Greek (``el``),
  Telugu (``te``), Tamil (``ta``), Chinese (``ch``, ``chinese_cht``),
  Japanese (``japan``)

.. warning::
   **PP-OCRv6 does NOT support Cyrillic, Arabic, Devanagari, Korean, Thai,
   Greek, Telugu, or Tamil.** If your document contains these scripts, use
   ``ocr_engine=paddle_v5`` (or ``tesseract`` with appropriate language
   packages installed).

.. seealso::
   * For instructions on adding support for a **new language** to Dedoc,
     see :ref:`add_language`.
   * For instructions on implementing a **custom OCR engine**, see
     :ref:`add_ocr_engine`.
   * For the full list of supported API parameters, see
     :ref:`api_parameters`.
