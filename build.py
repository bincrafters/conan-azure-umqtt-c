from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="Azure-uMQTT-C:shared", pure_c=True)
    # Skip static library
    if platform.system() == "Linux":
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if options["Azure-uMQTT-C:shared"]:
                 filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds
    builder.run()
