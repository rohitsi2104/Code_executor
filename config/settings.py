# import os
# import socket

# # ── API host/port config ──
# API_HOST = os.getenv("API_HOST", "0.0.0.0")
# API_PORT = int(os.getenv("API_PORT", 8080))

# # ── Security hardening imports ──
# try:
#     import prctl
#     import seccomp
# except ImportError:
#     prctl = None
#     seccomp = None

# def harden_process():
#     """
#     Drop all Linux capabilities and set no_new_privs.
#     """
#     if prctl is None:
#         return

#     # Prevent any execve from gaining privileges
#     prctl.set_no_new_privs(True)

#     # Drop every capability
#     for cap in prctl.available_capabilities():
#         prctl.capbset_drop(cap)

# def apply_seccomp_filter():
#     """
#     Install a seccomp filter that KILLs the process on any disallowed syscall.
#     """
#     if seccomp is None:
#         return

#     # Default action: kill the process
#     f = seccomp.SyscallFilter(defaction=seccomp.KILL)

#     # Minimal whitelist for Python & Uvicorn
#     whitelist = [
#         "read", "write", "exit", "rt_sigreturn", "rt_sigprocmask",
#         "futex", "sched_yield", "nanosleep", "clone", "execve",
#         "openat", "close", "brk", "mmap", "mprotect", "munmap",
#         "access", "arch_prctl", "set_tid_address", "set_robust_list",
#         "prlimit64", "getrandom", "socket", "connect", "recvfrom",
#         "sendto", "shutdown", "accept", "bind", "listen",
#         "getsockname", "getpeername", "fcntl", "lseek", "getcwd",
#         "stat", "fstat", "lstat", "unlink", "mkdir", "rt_sigaction",
#         "getpid", "pipe", "dup", "dup2", "getuid", "geteuid",
#         "getgid", "getegid", "prctl"
#     ]
#     for name in whitelist:
#         try:
#             f.add_rule(seccomp.ALLOW, name)
#         except Exception:
#             # some platforms may not support all syscalls
#             pass

#     f.load()

# def disable_dns_lookups():
#     """
#     Monkey-patch socket.getaddrinfo so DNS lookups always fail.
#     """
#     def _fail(*args, **kwargs):
#         raise OSError("DNS lookups are disabled by policy")
#     socket.getaddrinfo = _fail

# def init_security():
#     """
#     Run all security hardening steps in the correct order.
#     """
#     harden_process()
#     apply_seccomp_filter()
#     disable_dns_lookups()





# config/settings.py
import os
import socket

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8080))

try:
    import prctl
    import seccomp
except ImportError:
    prctl = None
    seccomp = None

def harden_process():
    if prctl is None:
        return
    prctl.set_no_new_privs(True)
    for cap in prctl.available_capabilities():
        prctl.capbset_drop(cap)

def apply_seccomp_filter():
    if seccomp is None:
        return

    # Be conservative: return EPERM instead of KILL while we stabilize
    f = seccomp.SyscallFilter(defaction=seccomp.ERRNO(1))

    whitelist = [
        # I/O & process
        "read","write","exit","rt_sigreturn","rt_sigprocmask","rt_sigaction",
        "futex","sched_yield","nanosleep","clone","execve","prctl",
        "getpid","getuid","geteuid","getgid","getegid","getrandom",

        # file / fs
        "openat","close","brk","mmap","mprotect","munmap","lseek",
        "getcwd","stat","fstat","lstat","unlink","mkdir","readlink","getdents64",

        # sockets
        "socket","connect","recvfrom","sendto","shutdown","accept","accept4","bind",
        "listen","getsockname","getpeername","fcntl","getsockopt","setsockopt",
        "sendmsg","recvmsg",

        # epoll/timer (uvicorn/asyncio)
        "epoll_create1","epoll_ctl","epoll_wait",
        "eventfd2","timerfd_create","timerfd_settime","restart_syscall",
    ]
    for name in whitelist:
        try:
            f.add_rule(seccomp.ALLOW, name)
        except Exception:
            pass

    f.load()

def disable_dns_lookups():
    def _fail(*args, **kwargs):
        raise OSError("DNS lookups are disabled by policy")
    socket.getaddrinfo = _fail

def init_security():
    harden_process()
    apply_seccomp_filter()
    # ⬇️ Only disable DNS if explicitly requested (for runners), NEVER by default
    if os.getenv("DISABLE_DNS", "0") == "1":
        disable_dns_lookups()
