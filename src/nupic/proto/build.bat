set PATH=%PATH%;H:\Projects\_CPPModules\capnproto.module\build.vs2015\Default

for /r %%v in (*.capnp) do capnp compile -oc++ "%%v" -I ../../

rem capnp compile -oc++ myproto.capnp