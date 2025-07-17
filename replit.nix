{ pkgs }: {
    deps = [
        pkgs.git-lfs
        # Add other dependencies here
    ];

    shellHook = ''
        # Commands to run when entering the shell
        echo "Welcome to your Replit shell!"
    '';
}