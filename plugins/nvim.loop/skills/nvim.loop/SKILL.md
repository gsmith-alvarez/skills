---
name: Neovim Loop (libuv) API
description: Reference for vim.loop / vim.uv (libuv) bindings in Neovim Lua — timers, spawned processes, filesystem, streams/pipes, OS queries, and handle lifecycle. Use when writing async I/O, timers, job runners, or file watchers.
---

# Neovim Loop (libuv) API Reference

Reference for Neovim's libuv bindings. In Neovim ≥ 0.10 they are exposed as `vim.uv`; the legacy alias `vim.loop` points at the same table (`vim.loop.new_timer()` works identically). Use these for any asynchronous work: timers, spawned processes, filesystem operations, streams, and OS queries. The event loop is driven by Neovim itself — you do **not** call `vim.uv.run()`.

Handle methods are shown in the idiomatic `handle:method(...)` form; the flat `vim.uv.method(handle, ...)` form also works.

---

## handle_lifecycle

Functions for managing any libuv handle's lifetime and the loop itself.

```lua
vim.uv.close({handle}, {callback})
vim.uv.ref({handle})
vim.uv.unref({handle})
vim.uv.has_ref({handle})
vim.uv.is_active({handle})
vim.uv.is_closing({handle})
vim.uv.walk({closure})
vim.uv.stop()
vim.uv.update_time()
vim.uv.run({mode})
vim.uv.loop_alive()
vim.uv.loop_close()
vim.uv.loop_configure({opt})
vim.uv.loop_mode()
vim.uv.print_all_handles()
vim.uv.print_active_handles()
vim.uv.cancel({handle})
```

---

## timer

`vim.uv.new_timer()` returns a timer handle. Methods:

```lua
vim.uv.new_timer()
function handle:start({timeout}, {repeat_}, {callback}) end
function handle:stop() end
function handle:again() end
function handle:set_repeat({delay}) end
function handle:get_repeat() end
function handle:get_due_in() end
```

---

## process

Spawn and control child processes.

```lua
vim.uv.spawn({path}, {options}, {on_exit})
function handle:kill({signum}) end
vim.uv.process_kill({handle}, {signum})
vim.uv.process_get_pid({handle})
vim.uv.get_process_title()
vim.uv.set_process_title({title})
```

---

## filesystem

Synchronous-style filesystem calls (`fs_*`); most take an optional callback for async use.

```lua
vim.uv.fs_access({path}, {mode})
vim.uv.fs_open({path}, {flags}, {mode})
vim.uv.fs_read({fd}, {size}, {offset})
vim.uv.fs_write({fd}, {data}, {offset})
vim.uv.fs_close({fd})
vim.uv.fs_stat({path})
vim.uv.fs_lstat({path})
vim.uv.fs_fstat({fd})
vim.uv.fs_fchmod({fd}, {mode})
vim.uv.fs_fchown({fd}, {uid}, {gid})
vim.uv.fs_fdatasync({fd})
vim.uv.fs_fsync({fd})
vim.uv.fs_ftruncate({fd}, {offset})
vim.uv.fs_futime({fd}, {atime}, {mtime})
vim.uv.fs_unlink({path})
vim.uv.fs_mkdir({path}, {mode})
vim.uv.fs_mkdtemp({tmpl})
vim.uv.fs_mkstemp({tmpl})
vim.uv.fs_rmdir({path})
vim.uv.fs_rename({path}, {new_path})
vim.uv.fs_copyfile({path}, {new_path}, {flags})
vim.uv.fs_chmod({path}, {mode})
vim.uv.fs_chown({path}, {uid}, {gid})
vim.uv.fs_lchown({path}, {uid}, {gid})
vim.uv.fs_lutime({path}, {atime}, {mtime})
vim.uv.fs_link({path}, {new_path})
vim.uv.fs_symlink({path}, {new_path}, {flags})
vim.uv.fs_readlink({path})
vim.uv.fs_realpath({path})
vim.uv.fs_sendfile({out_fd}, {in_fd}, {in_offset}, {length})
vim.uv.fs_statfs({path})
vim.uv.fs_scandir({path})
vim.uv.fs_scandir_next({dir})
vim.uv.fs_opendir({path}, {entries}, {flags})
vim.uv.fs_readdir({dir})
vim.uv.fs_closedir({dir})
```

### fs event / fs poll watchers

```lua
vim.uv.new_fs_event()
function handle:start({path}, {flags}, {callback}) end
function handle:stop() end
function handle:getpath() end
vim.uv.new_fs_poll()
function handle:start({path}, {interval}, {callback}) end
function handle:stop() end
function handle:getpath() end
```

---

## stream_pipe

Pipe (unnamed/named) handles and their constructors.

```lua
vim.uv.new_pipe({readable})
vim.uv.pipe({readfd}, {writefd})
vim.uv.pipe_open({handle}, {fd})
vim.uv.pipe_bind({handle}, {name})
vim.uv.pipe_bind2({handle}, {a}, {b})
vim.uv.pipe_connect({handle}, {name}, {callback})
vim.uv.pipe_connect2({handle}, {a}, {b}, {callback})
vim.uv.pipe_getpeername({handle})
vim.uv.pipe_getsockname({handle})
vim.uv.pipe_pending_instances({handle}, {n})
vim.uv.pipe_pending_count({handle})
vim.uv.pipe_pending_type({handle})
vim.uv.pipe_chmod({handle}, {mode})
```

---

## tcp

```lua
vim.uv.new_tcp()
function handle:open({sock}) end
function handle:bind({addr}, {port}) end
function handle:connect({addr}, {port}, {callback}) end
function handle:close_reset({callback}) end
function handle:getpeername() end
function handle:getsockname() end
function handle:keepalive({enable}, {delay}) end
function handle:nodelay({enable}) end
function handle:simultaneous_accepts({enable}) end
function handle:write_queue_size() end
```

---

## udp

```lua
vim.uv.new_udp()
function handle:open({fd}) end
function handle:bind({addr}, {port}, {opts}) end
function handle:connect({addr}, {port}) end
function handle:recv_start({callback}) end
function handle:recv_stop() end
function handle:send({data}, {addr}, {port}, {callback}) end
function handle:try_send({data}, {addr}, {port}) end
function handle:try_send2({data}, {addr}, {port}) end
function handle:getpeername() end
function handle:getsockname() end
function handle:set_broadcast({enable}) end
function handle:set_membership({group}, {iface}, {membership}) end
function handle:set_multicast_interface({iface}) end
function handle:set_multicast_loop({enable}) end
function handle:set_multicast_ttl({ttl}) end
function handle:set_source_membership({group}, {iface}, {source}, {membership}) end
function handle:set_ttl({ttl}) end
function handle:get_send_queue_size() end
function handle:get_send_queue_count() end
```

---

## tty

```lua
vim.uv.new_tty({fd}, {readable})
function handle:set_mode({mode}) end
function handle:get_winsize() end
vim.uv.tty_get_vterm_state()
vim.uv.tty_set_vterm_state({state})
vim.uv.tty_reset_mode()
```

---

## stream_methods

Shared stream methods (pipes, tcp, udp, tty all implement these).

```lua
function handle:read_start({callback}) end
function handle:read_stop() end
function handle:write({data}, {callback}) end
function handle:write2({data}, {send_handle}, {callback}) end
function handle:try_write({data}) end
function handle:try_write2({data}, {send_handle}) end
function handle:shutdown({callback}) end
function handle:is_readable() end
function handle:is_writable() end
function handle:get_write_queue_size() end
function handle:set_blocking({blocking}) end
function handle:listen({backlog}, {callback}) end
function handle:accept({client}) end
function handle:recv_buffer_size({size}) end
function handle:send_buffer_size({size}) end
```

---

## signal

```lua
vim.uv.new_signal()
function handle:start({signum}, {callback}) end
function handle:start_oneshot({signum}, {callback}) end
function handle:stop() end
```

---

## async_idle_prepare_check_poll

Async, idle, prepare, check, and poll handles for hooking the loop.

```lua
vim.uv.new_async({callback})
function handle:send({data}) end
vim.uv.new_idle()
function handle:start({callback}) end
function handle:stop() end
vim.uv.new_prepare()
function handle:start({callback}) end
function handle:stop() end
vim.uv.new_check()
function handle:start({callback}) end
function handle:stop() end
vim.uv.new_poll({fd})
function handle:start({events}, {callback}) end
function handle:stop() end
vim.uv.new_socket_poll({fd})
```

---

## thread_work

Off-thread work and synchronization (use for blocking CPU/IO off the main loop).

```lua
vim.uv.new_work({work_cb}, {after_work_cb})
vim.uv.queue_work({work})
vim.uv.new_thread({cb}, {...})
vim.uv.thread_self()
vim.uv.thread_equal({t1}, {t2})
vim.uv.thread_join({thread})
vim.uv.thread_detach({thread})
vim.uv.thread_getname({thread})
vim.uv.thread_setname({thread}, {name})
vim.uv.thread_getpriority({thread})
vim.uv.thread_setpriority({thread}, {priority})
vim.uv.thread_getcpu()
vim.uv.thread_getaffinity({thread})
vim.uv.thread_setaffinity({thread}, {affinity})
vim.uv.new_sem()
vim.uv.sem_post({sem})
vim.uv.sem_trywait({sem})
vim.uv.sem_wait({sem})
```

---

## os

Process/environment/OS queries.

```lua
vim.uv.os_getenv({name})
vim.uv.os_setenv({name}, {value})
vim.uv.os_unsetenv({name})
vim.uv.os_environ()
vim.uv.os_homedir()
vim.uv.os_tmpdir()
vim.uv.os_getpid()
vim.uv.os_getppid()
vim.uv.os_getpriority({pid})
vim.uv.os_setpriority({pid}, {priority})
vim.uv.os_get_passwd()
vim.uv.os_uname()
vim.uv.os_gethostname()
vim.uv.cwd()
vim.uv.chdir({dir})
vim.uv.getgid()
vim.uv.getuid()
vim.uv.setgid({id})
vim.uv.setuid({id})
vim.uv.getaddrinfo({node}, {service}, {opts}, {callback})
vim.uv.getnameinfo({addr}, {opts}, {callback})
```

---

## misc

Remaining helpers: time, memory, errors, networking, encoding, and version.

```lua
vim.uv.hrtime()
vim.uv.now()
vim.uv.sleep({msec})
vim.uv.uptime()
vim.uv.loadavg()
vim.uv.get_free_memory()
vim.uv.get_total_memory()
vim.uv.get_available_memory()
vim.uv.get_constrained_memory()
vim.uv.getrusage()
vim.uv.getrusage_thread()
vim.uv.gettimeofday()
vim.uv.cpu_info()
vim.uv.clock_gettime({clock})
vim.uv.guess_handle({fd})
vim.uv.handle_get_type({handle})
vim.uv.req_get_type({req})
vim.uv.kill({pid}, {signum})
vim.uv.errno()
vim.uv.constants
vim.uv.translate_sys_error({err})
vim.uv.available_parallelism()
vim.uv.backend_fd()
vim.uv.backend_timeout()
vim.uv.disable_stdio_inheritance()
vim.uv.exepath({path})
vim.uv.fileno({handle})
vim.uv.if_indextoiid({ifindex})
vim.uv.if_indextoname({ifindex})
vim.uv.interface_addresses()
vim.uv.random({buf}, {size}, {flags}, {callback})
vim.uv.socketpair({a}, {b})
vim.uv.version()
vim.uv.version_string()
vim.uv.utf16_to_wtf8({...)
vim.uv.wtf8_to_utf16({...)
vim.uv.utf16_length_as_wtf8({...)
vim.uv.wtf8_length_as_utf16({...)
```
