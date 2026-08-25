from pystructurizr.dsl import Workspace

with Workspace() as workspace:
    with workspace.Model(name = "Expense Management System") as model:
        # Users
        manager = model.Person(
            name="Household Manager",
            description="The primary user responsible for tracking and analyzing home expenses."
        )

        # External systems
        lidl_receipts = model.SoftwareSystem(
            name="Lidl database",
            description="The Lidl database system where the user's receipts are stored via app.",
            # technology="Lidl API",
            tags=["External", "database"]
        )

        mail_receipts = model.SoftwareSystem(
            name="Gmail receipts account",
            description="The Gmail account used to receive purchase receipts.",
            # technology="IMAP",
            tags=["External", "Web Browser"]
        )

        message_delivery = model.SoftwareSystem(
            name="Mobile Message Delivery System",
            description="Whatsapp messaging service used to send alerts and updates to the user.",
            # technology="Whatsapp API",
            tags=["External", "MobileApp"]
        )

        mecadona_system = model.SoftwareSystem(
            name="Mecadona automated receipts delivery system",
            description="The Mecadona software system that sends the user's receipts to an email per purchase.",
            # technology="email",
            tags=["External"]
        )

        # Internal Systems
        system = model.SoftwareSystem(
            name="Expense Management System",
            description="Automates the collection and reporting of household costs."
        )

        # Relationships
        manager.uses(mail_receipts, "Sends purchase receipts to")
        system.uses(mail_receipts, "Fetches receipts from", technology="IMAP")
        system.uses(lidl_receipts, "Fetches receipts from", technology="Lidl API")
        system.uses(message_delivery, "Sends alerts and updates via", technology="Whatsapp API")
        message_delivery.uses(manager, "Delivers notifications to")
        mecadona_system.uses(mail_receipts, "Sends receipts to", technology="email")

    # View Definition
    landscape = workspace.SystemLandscapeView(
        name="SystemLandscapeView",
        description="System Landscape Diagram for the Expense Management System, showing the system and its external interactions."
    )

    workspace.Styles(
        # External Boundaries (Muted grey to indicate lack of control)
        {"tag": "External" ,"background": "#999999", "color": "#ffffff", "stroke": "#000000"},
        {"tag": "MobileApp", "shape": "MobileDevicePortrait"}
    )
