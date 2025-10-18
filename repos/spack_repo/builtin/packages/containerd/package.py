from spack.package import *


class Containerd(MakefilePackage):
    """An open and reliable container runtime with emphasis on simplicity,
    robustness, and portability. Provides core container lifecycle management
    and is a graduated CNCF project."""

    homepage = "https://containerd.io"
    url      = "https://github.com/containerd/containerd/archive/refs/tags/v2.1.4.tar.gz"
    git      = "https://github.com/containerd/containerd.git"

    maintainers = ["spack-maintainers"]

    license("Apache-2.0")

    version("2.1.4", sha256="75cb2b7193e4e490e9fbdc236c0e811ccaba3376")

    # Build dependencies
    depends_on("go@1.23:", type="build")
    depends_on("pkg-config", type="build")

    # Variants reflecting Makefile targets and optional features
    variant("cri", default=True, description="Enable CRI plugin for Kubernetes")
    variant("btrfs", default=False, description="Enable btrfs snapshotter support")
    variant("aufs", default=False, description="Enable aufs snapshotter support (deprecated)")
    variant("seccomp", default=True, description="Enable seccomp support")
    variant("apparmor", default=True, description="Enable AppArmor support")
    variant("systemd", default=True, description="Enable systemd cgroup support")

    # Platform-specific considerations
    conflicts("+apparmor", when="platform=darwin", msg="AppArmor only available on Linux")
    conflicts("+systemd", when="platform=darwin", msg="systemd only available on Linux")

    build_targets = []

    def edit(self, spec, prefix):
        # Containerd uses Makefiles like Makefile.linux, Makefile.darwin, etc.
        if spec.satisfies("platform=linux"):
            self.build_targets.append("-f Makefile.linux")
        elif spec.satisfies("platform=darwin"):
            self.build_targets.append("-f Makefile.darwin")
        elif spec.satisfies("platform=windows"):
            self.build_targets.append("-f Makefile.windows")

        # Add feature flags based on variants
        if "+cri" in spec:
            self.build_targets.append("BUILDTAGS+=cri")
        if "+btrfs" in spec:
            self.build_targets.append("BUILDTAGS+=btrfs")
        if "+aufs" in spec:
            self.build_targets.append("BUILDTAGS+=aufs")
        if "+seccomp" in spec:
            self.build_targets.append("BUILDTAGS+=seccomp")
        if "+apparmor" in spec:
            self.build_targets.append("BUILDTAGS+=apparmor")
        if "+systemd" in spec:
            self.build_targets.append("BUILDTAGS+=systemd")

    def install(self, spec, prefix):
        make("install", *self.build_targets, "PREFIX={0}".format(prefix))