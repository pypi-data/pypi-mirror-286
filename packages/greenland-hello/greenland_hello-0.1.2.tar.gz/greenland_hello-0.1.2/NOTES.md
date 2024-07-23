
# Codeberg doesn't host CI

See https://docs.codeberg.org/ci/actions/. I understand this as
codeberg not hosting CI from Forgejo actions. I'd have to provide a
run as callback, which I am frankly not ready to do (security!).

If I have to run anything at my side anyway I can run a test framework
or a CI pipeline (like Zuul) locally and merge the test status /
reports to the repository in a suitable fashion (that has to be
decided yet).
