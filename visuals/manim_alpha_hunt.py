from manim import *

BG = "#050a10"
TEAL = "#2dd4bf"
GREEN = "#34d399"
AMBER = "#f59e0b"
RED = "#fb7185"
BLUE = "#60a5fa"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"
MONO = "DejaVu Sans Mono"


def title(s, color=TEAL):
    t = Text(s, font=MONO, font_size=42, color=color, weight=BOLD)
    if t.width > 12:
        t.scale_to_fit_width(12)
    return t


def card(label, body, color=TEAL):
    box = RoundedRectangle(width=3.0, height=1.55, corner_radius=0.18, color=color, fill_color="#0d1b26", fill_opacity=0.92)
    h = Text(label, font=MONO, font_size=22, color=color, weight=BOLD).move_to(box.get_center()+UP*0.38)
    b = Text(body, font=MONO, font_size=17, color=TEXT, line_spacing=0.8).move_to(box.get_center()+DOWN*0.22)
    return VGroup(box, h, b)


def fade_all(scene):
    if scene.mobjects:
        scene.play(FadeOut(Group(*scene.mobjects)), run_time=0.6)
        scene.wait(0.2)


class AlphaHuntFourLoopOrbit(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = title("Daily Alpha Hunt")
        sub = Text("Four boring jobs that compound evidence", font=MONO, font_size=24, color=MUTED).next_to(t, DOWN)
        self.play(Write(t), FadeIn(sub, shift=UP), run_time=1.4)
        self.wait(0.7)
        self.play(VGroup(t, sub).animate.to_edge(UP, buff=0.45), run_time=0.8)

        nodes = VGroup(
            card("1 SOURCES", "OpenAlex\nCrossref\narXiv", TEAL),
            card("2 HARVEST", "rank board\nchoose next", AMBER),
            card("3 CHEAP TEST", "fixed config\nspread paid", GREEN),
            card("4 MEMORY", "ledger\ngraveyard", RED),
        ).arrange(RIGHT, buff=0.45).move_to(ORIGIN)
        arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i+1].get_left(), buff=0.12, color=MUTED) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(n, shift=UP*0.25) for n in nodes], lag_ratio=0.2), run_time=2.0)
        self.play(Create(arrows), run_time=1.2)
        self.wait(0.6)

        seed = Dot(nodes[0].get_center(), color=TEAL).scale(1.4)
        self.play(FadeIn(seed), run_time=0.4)
        for i, n in enumerate(nodes[1:], start=1):
            self.play(seed.animate.move_to(n.get_center()), n[0].animate.set_stroke(width=5), run_time=1.0)
            self.play(n[0].animate.set_stroke(width=2), run_time=0.3)
        loop_arrow = CurvedArrow(nodes[-1].get_bottom(), nodes[0].get_bottom(), angle=-TAU/3, color=BLUE)
        self.play(Create(loop_arrow), FadeOut(seed), run_time=1.4)
        final = Text("Seed -> Score -> Falsify -> Test -> Distill -> Ship or Kill", font=MONO, font_size=24, color=TEXT).to_edge(DOWN, buff=0.55)
        final_bg = BackgroundRectangle(final, color=BG, fill_opacity=0.88, buff=0.14)
        self.play(FadeIn(final_bg), Write(final), run_time=1.2)
        self.wait(2.0)
        fade_all(self)


class AlphaHuntCheapExperimentGauntlet(Scene):
    def construct(self):
        self.camera.background_color = BG
        t = title("Cheap Experiment Gauntlet", GREEN).to_edge(UP, buff=0.45)
        self.play(Write(t), run_time=1.0)
        paper = card("PAPER SEED", "session spillover\ncontinuation/fade", TEAL).move_to(LEFT*4.2+UP*1.0)
        checklist = VGroup(
            Text("observable exists", font=MONO, font_size=20, color=TEXT),
            Text("no leakage", font=MONO, font_size=20, color=TEXT),
            Text("costs included", font=MONO, font_size=20, color=TEXT),
            Text("kill criteria", font=MONO, font_size=20, color=TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(paper, RIGHT, buff=0.8)
        self.play(FadeIn(paper, shift=RIGHT), run_time=1.0)
        self.play(LaggedStart(*[Write(x) for x in checklist], lag_ratio=0.25), run_time=1.6)
        lock = Text("CONFIG LOCKED", font=MONO, font_size=28, color=AMBER, weight=BOLD).move_to(RIGHT*3.7+UP*1.0)
        slash = Text("no retune rescue", font=MONO, font_size=22, color=RED).next_to(lock, DOWN)
        self.play(Write(lock), FadeIn(slash), run_time=1.0)
        self.wait(0.6)

        bench = RoundedRectangle(width=10.5, height=2.4, corner_radius=0.2, color=GREEN, fill_color="#0d1b26", fill_opacity=0.85).shift(DOWN*1.05)
        axis = Line(bench.get_left()+RIGHT*0.6, bench.get_right()+LEFT*0.6, color=MUTED).shift(DOWN*0.1)
        bars = VGroup()
        for i in range(32):
            x = axis.get_left()[0] + i*(axis.width/31)
            h = 0.2 + 0.75*abs(np.sin(i/4))
            bars.add(Line([x, axis.get_y()-h/2, 0], [x, axis.get_y()+h/2, 0], color=TEAL if i < 17 else AMBER, stroke_width=4))
        split = DashedLine([0, bench.get_bottom()[1]+0.25, 0], [0, bench.get_top()[1]-0.25, 0], color=RED)
        self.play(FadeIn(bench), Create(axis), run_time=0.8)
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.03), Create(split), run_time=2.0)
        gates = VGroup(
            card("GATE 1", "spread paid", GREEN),
            card("GATE 2", "split stable", AMBER),
            card("GATE 3", "beats null", RED),
        ).scale(0.72).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.4)
        self.play(LaggedStart(*[FadeIn(g, shift=UP*0.2) for g in gates], lag_ratio=0.2), run_time=1.4)
        stamp = Text("DEFAULT: KILL", font=MONO, font_size=42, color=RED, weight=BOLD).move_to(ORIGIN+DOWN*0.05)
        self.play(Write(stamp), run_time=1.0)
        self.wait(1.5)
        final = Text("The package worked if one verdict became sharper.", font=MONO, font_size=24, color=TEXT).next_to(stamp, DOWN, buff=0.35)
        self.play(FadeIn(final), run_time=0.8)
        self.wait(2.0)
        fade_all(self)
