async def on_startup(app):
    app["background_tasks"] = [
        app.loop.create_task(i) for i in app["background_futures"]
    ]
