#include <linux/module.h>
#include <linux/export-internal.h>
#include <linux/compiler.h>

MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};


MODULE_INFO(depends, "drm_kms_helper,usbcore,drm,drm_client_lib,drm_shmem_helper");

MODULE_ALIAS("usb:v534Dp6021d*dc*dsc*dp*icFFisc00ip00in*");
MODULE_ALIAS("usb:v534Dp0821d*dc*dsc*dp*icFFisc00ip00in*");
MODULE_ALIAS("usb:v345Fp9132d*dc*dsc*dp*icFFisc00ip00in*");
MODULE_ALIAS("usb:v345Fp9133d*dc*dsc*dp*icFFisc00ip00in*");
