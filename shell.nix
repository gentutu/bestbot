with (import <nixpkgs> {});
mkShell {
  buildInputs = with pkgs; [
    python39
  ];
  nativeBuildInputs = with pkgs.python39Packages; [
    discordpy
    requests
  ];
}
