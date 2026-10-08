"""Tests for doctor.py, run against throwaway skill repos.
Usage: python3 -m unittest scripts/test_doctor.py
"""
import pathlib, subprocess, sys, tempfile, textwrap, unittest

DOCTOR = pathlib.Path(__file__).with_name("doctor.py")


def skill(name, body="Do the thing.", desc='"Use when testing."', fm_name=None):
    return f"---\nname: {fm_name or name}\ndescription: {desc}\n---\n\n{body}\n"


class Doctor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name)
        self.add("alpha")
        self.add("beta", body="Then use `alpha`.")

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, name, where="dev-skills", **kw):
        d = self.repo / where / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(skill(name, **kw))
        self.write_readme()

    def write_readme(self, extra=()):
        names = sorted(p.name for p in (self.repo / "dev-skills").iterdir() if (p / "SKILL.md").exists())
        rows = "\n".join(f"| {n} | does {n} |" for n in [*names, *extra])
        (self.repo / "dev-skills" / "README.md").write_text(f"# dev-skills\n\n| Skill | Use |\n|---|---|\n{rows}\n")

    def run_doctor(self):
        r = subprocess.run([sys.executable, DOCTOR, self.repo], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def assertFails(self, needle):
        code, out = self.run_doctor()
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)

    def test_clean_repo_passes(self):
        code, out = self.run_doctor()
        self.assertEqual(code, 0, out)

    def test_name_must_match_folder(self):
        self.add("gamma", fm_name="gama")
        self.assertFails("gamma/SKILL.md")

    def test_missing_frontmatter(self):
        (self.repo / "dev-skills" / "alpha" / "SKILL.md").write_text("no frontmatter\n")
        self.assertFails("no frontmatter")

    def test_unquoted_description_with_colon_space_is_invalid_yaml(self):
        self.add("gamma", desc="Use when: testing")
        self.assertFails("invalid YAML")

    def test_long_description(self):
        self.add("gamma", desc='"' + "x" * 1100 + '"')
        self.assertFails("1024")

    def test_portable_skill_naming_a_model_fails(self):
        self.add("gamma", body="Review with model `gpt-6.1-sol`.")
        self.assertFails("gpt-6.1-sol")

    def test_portable_skill_naming_a_cli_fails(self):
        self.add("gamma", body="Run `codex exec` at the root.")
        self.assertFails("codex exec")

    def test_portable_reference_file_is_scanned(self):
        ref = self.repo / "dev-skills" / "alpha" / "references"
        ref.mkdir()
        (ref / "x.md").write_text("Serve it with tailscale serve.\n")
        self.assertFails("tailscale")

    def test_non_portable_folder_may_name_tools(self):
        self.add("writer", where="personal", body="Use `codex exec`.")
        code, out = self.run_doctor()
        self.assertEqual(code, 0, out)

    def test_route_to_missing_skill_fails(self):
        self.add("gamma", body="Follow `delta-skill` first.")
        self.assertFails("delta-skill")

    def test_dev_skill_missing_from_readme_fails(self):
        self.add("gamma")
        self.write_readme()
        readme = self.repo / "dev-skills" / "README.md"
        readme.write_text(readme.read_text().replace("| gamma | does gamma |\n", ""))
        self.assertFails("not listed in dev-skills/README.md")

    def test_readme_listing_deleted_skill_fails(self):
        self.write_readme(extra=["ghost"])
        self.assertFails("ghost")

    def test_long_skill_only_warns(self):
        self.add("gamma", body="word " * 1500)
        code, out = self.run_doctor()
        self.assertEqual(code, 0, out)
        self.assertIn("WARN", out)

    def test_empty_description_fails(self):
        self.add("gamma", desc="")
        self.assertFails("no description")

    def test_long_block_description_fails(self):
        self.add("gamma", desc="|\n  " + "x" * 1100)
        self.assertFails("1024")

    def test_block_description_may_contain_colon_space(self):
        self.add("gamma", desc=">\n  Use when: testing")
        code, out = self.run_doctor()
        self.assertEqual(code, 0, out)

    def test_model_name_in_description_fails(self):
        self.add("gamma", desc='"Review with gpt-6.1-sol."')
        self.assertFails("gpt-6.1-sol")

    def test_reference_loading_missing_skill_fails(self):
        ref = self.repo / "dev-skills" / "alpha" / "references"
        ref.mkdir()
        (ref / "x.md").write_text("Load `gone-skill` first.\n")
        self.assertFails("gone-skill")

    def test_single_word_skill_after_load_fails(self):
        self.add("gamma", body="Load `ghost` first.")
        self.assertFails("ghost")

    def test_tool_name_after_use_is_not_a_route(self):
        self.add("gamma", body="Prefer to use `gh` for this.")
        code, out = self.run_doctor()
        self.assertEqual(code, 0, out)

    def test_stale_readme_fails_even_with_no_dev_skills(self):
        for n in ("alpha", "beta"):
            (self.repo / "dev-skills" / n / "SKILL.md").unlink()
        self.assertFails("alpha")

    def test_comment_only_description_fails(self):
        self.add("gamma", desc="# no value")
        self.assertFails("no description")

    def test_long_multiline_quoted_description_fails(self):
        self.add("gamma", desc='"' + "x" * 600 + "\n  " + "y" * 600 + '"')
        self.assertFails("1024")

    def test_long_block_description_with_blank_line_fails(self):
        self.add("gamma", desc="|\n  " + "x" * 600 + "\n\n  " + "y" * 600)
        self.assertFails("1024")

    def test_use_the_named_skill_route_fails(self):
        self.add("gamma", body="Use the `gone-skill` skill.")
        self.assertFails("gone-skill")

    def test_harness_name_in_portable_text_fails(self):
        self.add("gamma", body="Review with Codex CLI.")
        self.assertFails("Codex")

    def scenario(self, folder, name="s", skill=None, task="Do it.", passif="- it works"):
        d = self.repo / "evals" / folder
        d.mkdir(parents=True, exist_ok=True)
        body = f"---\nskill: {skill or folder}\n---\n"
        if task is not None:
            body += f"## Task\n{task}\n\n"
        if passif is not None:
            body += f"## Pass if\n{passif}\n"
        (d / f"{name}.md").write_text(body)

    def test_valid_scenario_passes(self):
        self.scenario("alpha")
        code, out = self.run_doctor()
        self.assertEqual(code, 0, out)

    def test_scenario_for_missing_skill_fails(self):
        self.scenario("ghost")
        self.assertFails("ghost")

    def test_scenario_skill_must_match_folder(self):
        self.scenario("alpha", skill="beta")
        self.assertFails("evals/alpha/s.md")

    def test_scenario_skill_must_be_plain(self):
        self.scenario("alpha", skill="'alpha'")
        self.assertFails("skill: alpha")

    def test_scenario_with_two_skill_lines_fails(self):
        d = self.repo / "evals" / "alpha"
        d.mkdir(parents=True, exist_ok=True)
        (d / "s.md").write_text("---\nskill: beta\nskill: alpha\n---\n## Task\nx\n\n## Pass if\n- y\n")
        self.assertFails("evals/alpha/s.md")

    def test_scenario_without_criteria_fails(self):
        self.scenario("alpha", passif=None)
        self.assertFails("Pass if")

    def test_scenario_with_empty_task_before_criteria_fails(self):
        self.scenario("alpha", task="")
        self.assertFails("Task")

    def test_scenario_without_task_fails(self):
        self.scenario("alpha", task=None)
        self.assertFails("Task")


if __name__ == "__main__":
    unittest.main()
