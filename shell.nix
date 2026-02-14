{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.psutil
  ];

  shellHook = ''
    echo "gamestart dev shell"
    echo "Run: python deadspace.py"
  '';
}
