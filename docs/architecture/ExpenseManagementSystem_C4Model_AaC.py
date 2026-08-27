from pystructurizr.dsl import Workspace

with Workspace() as workspace:
    with workspace.Model(name = "Expense Management System") as model:
       # 1. Actors
        manager = model.Person(
            name="Household Manager",
            description="Responsible for tracking and analyzing home expenses.",
        )

        # 2. External Systems
        email_server = model.SoftwareSystem(
            name="External Email Mailbox",
            description="Dedicated IMAP/SMTP server storing inbound receipts and delivering outbound ledgers.",
            tags=["External"],
        )

        mercadona_system = model.SoftwareSystem(
            name="Mercadona E-Receipt Service",
            description="Dispatches automated purchase invoice PDFs to the user's dedicated mailbox.",
            tags=["External"],
        )

        lidl_system = model.SoftwareSystem(
            name="Lidl Plus Platform",
            description="Mobile retail backend storing digital customer purchase receipts.",
            tags=["External"],
        )

        # 3. Main Software System
        appliance = model.SoftwareSystem(
            name="Expense Management System",
            description="Automates ingestion, VLM extraction, entity resolution, and BI reporting.",
        )

        # 4. Containers
        processor_pipeline = appliance.Container(
            name="Receipt Processor Pipeline",
            description="Monthly scheduled batch runner executing ingestion, vLLM extraction, embedding resolution, and report generation.",
            technology="Python 3.12 / ZenML / vLLM / Docker",
            tags=["BatchProcess"],
        )

        ui = appliance.Container(
            name="BI & Dashboard UI",
            description="Presents analytical charts from DuckDB and hosts interactive single-receipt ML demo.",
            technology="Python 3.12 / Streamlit / Docker",
            tags = ["WebApplication"]
        )

        # 5. Data & Metadata Storage
        with model.Group("Data & Metadata Storage") as data_stores:
            lakehouse = appliance.Container(
                name="Analytical Lakehouse Store",
                description="Houses normalized items, master taxonomy, vector embeddings, and analytical SQL views.",
                technology="DuckDB / Local Parquet Storage",
                tags=["database"]
            )

            blob_store = appliance.Container(
                name="Unstructured Blob Store",
                description="Stores versioned raw receipt images/PDFs and remote Parquet database backups.",
                technology="DVC / Cloudflare R2",
                tags=["database"]
            )

            mlflow_store = appliance.Container(
                name="ML Metadata & Experiment Registry",
                description="Logs run executions, extraction metrics, prompts, and embedding parameters.",
                technology="MLflow / SQLite",
                tags=["database"]
            )

        # 6. Relationships

        # External -> External
        mercadona_system.uses(
            email_server,
            "Delivers purchase invoice PDFs to",
            technology="SMTP",
        )
        # Person -> Systems / Containers
        manager.uses(
            email_server,
            "Forwards ad-hoc receipt images/PDFs to",
            technology="SMTP",
        )
        manager.uses(
            email_server,
            "Reads monthly spending report and downloads ledger from",
            technology="IMAP / Mail Client",
        )
        manager.uses(
            ui,
            "Explores financial BI analytics and tests live ML inference on",
            technology="HTTPS",
        )

        # Pipeline Container -> External & Storage
        processor_pipeline.uses(
            email_server,
            "Fetches unread receipt attachments from (last 30 days)",
            technology="IMAP / TLS",
        )
        processor_pipeline.uses(
            lidl_system,
            "Polls digital invoices via authenticated sync worker from",
            technology="HTTPS / REST",
        )
        processor_pipeline.uses(
            blob_store,
            "Stages, hashes, and syncs raw invoice blobs to",
            technology="DVC / S3 API",
        )
        processor_pipeline.uses(
            lakehouse,
            "Appends normalized tabular records and vector embeddings to",
            technology="DuckDB In-Process API",
        )
        processor_pipeline.uses(
            mlflow_store,
            "Logs run telemetry, prompt versions, and token metrics to",
            technology="MLflow Client / IPC",
        )
        processor_pipeline.uses(
            blob_store,
            "Exports partitioned Parquet disaster recovery snapshots to",
            technology="DuckDB httpfs / S3 API",
        )
        processor_pipeline.uses(
            email_server,
            "Dispatches generated .xlsx workbook and spending summary via",
            technology="SMTP / TLS",
        )

        # UI Container -> Storage
        ui.uses(
            lakehouse,
            "Queries aggregated metrics and category breakdowns from",
            technology="DuckDB In-Process API (Read-Only)",
        )

    # 7. Views
    landscape = workspace.SystemLandscapeView(
        name="SystemLandscapeView",
        description="System Landscape Diagram for the Expense Management System and its external ecosystem.",
    )

    container_view = workspace.ContainerView(
        element=appliance,
        name="ContainerView",
        description="Container Diagram showing compute boundaries and persistent data stores.",
    )

    # 8. Styles
    workspace.Styles(
        {"tag": "External" ,"background": "#999999", "color": "#ffffff", "stroke": "#000000"},
        {"tag": "WebApplication", "shape": "WebBrowser"},
    )
