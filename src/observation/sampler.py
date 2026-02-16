class AdaptiveSampler:
    def __init__(self, cfg):
        self.cfg = cfg
        self.current_fps = cfg.get("fps_explore", 1)

    def next_fps(self, scene: str):
        if scene == "battle":
            self.current_fps = self.cfg.get("fps_battle", 5)
        elif scene == "menu":
            self.current_fps = self.cfg.get("fps_menu", 5)
        elif scene == "boost":
            self.current_fps = self.cfg.get("fps_boost", 10)
        else:
            self.current_fps = self.cfg.get("fps_explore", 1)
        return self.current_fps
