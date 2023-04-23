{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.poetry
    pkgs.python310Packages.virtualenv
    pkgs.jupyter
    pkgs.graphviz
  ];

  shellHook = ''
    poetry install
  '';
}
