/* src/config.h.  Generated from config.h.in by configure.  */
/* src/config.h.in.  Generated from configure.ac by autoheader.  */

#ifndef LIBWALLYCORE_CONFIG_H
#define LIBWALLYCORE_CONFIG_H

/* Define if building universal (internal helper macro) */
/* #undef AC_APPLE_UNIVERSAL_BUILD */

/* Define to 1 if you have the <asm/page.h> header file. */
/* #undef HAVE_ASM_PAGE_H */

/* Define to 1 if you have the <byteswap.h> header file. */
#define HAVE_BYTESWAP_H 1

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the `explicit_bzero' function. */
#define HAVE_EXPLICIT_BZERO 1

/* Define to 1 if you have the `explicit_memset' function. */
/* #undef HAVE_EXPLICIT_MEMSET */

/* inline asm code can be used */
#define HAVE_INLINE_ASM 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define to 1 if you have the <mbedtls/sha256.h> header file. */
/* #undef HAVE_MBEDTLS_SHA256_H */

/* Define to 1 if you have the <mbedtls/sha512.h> header file. */
/* #undef HAVE_MBEDTLS_SHA512_H */

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Define to 1 if you have the `memset_s' function. */
/* #undef HAVE_MEMSET_S */

/* Define if we have mmap */
#define HAVE_MMAP 1

/* Define if we have posix_memalign */
#define HAVE_POSIX_MEMALIGN 1

/* Define if we have pthread support */
#define HAVE_PTHREAD 1

/* Have PTHREAD_PRIO_INHERIT. */
#define HAVE_PTHREAD_PRIO_INHERIT 1

/* If available, contains the Python version number currently in use. */
#define HAVE_PYTHON "3.9"

/* Define to 1 if you have the `secp256k1_ecdh' function. */
/* #undef HAVE_SECP256K1_ECDH */

/* Define to 1 if you have the `secp256k1_ecdsa_recover' function. */
/* #undef HAVE_SECP256K1_ECDSA_RECOVER */

/* Define to 1 if you have the `secp256k1_ecdsa_s2c_sign' function. */
/* #undef HAVE_SECP256K1_ECDSA_S2C_SIGN */

/* Define to 1 if you have the `secp256k1_generator_parse' function. */
/* #undef HAVE_SECP256K1_GENERATOR_PARSE */

/* Define to 1 if you have the `secp256k1_rangeproof_verify' function. */
/* #undef HAVE_SECP256K1_RANGEPROOF_VERIFY */

/* Define to 1 if you have the `secp256k1_schnorrsig_verify' function. */
/* #undef HAVE_SECP256K1_SCHNORRSIG_VERIFY */

/* Define to 1 if you have the `secp256k1_surjectionproof_initialize'
   function. */
/* #undef HAVE_SECP256K1_SURJECTIONPROOF_INITIALIZE */

/* Define to 1 if you have the `secp256k1_whitelist_sign' function. */
/* #undef HAVE_SECP256K1_WHITELIST_SIGN */

/* Define to 1 if you have the `secp256k1_xonly_pubkey_parse' function. */
/* #undef HAVE_SECP256K1_XONLY_PUBKEY_PARSE */

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the <sys/mman.h> header file. */
#define HAVE_SYS_MMAN_H 1

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define if we have unaligned access */
#define HAVE_UNALIGNED_ACCESS 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Define to the sub-directory where libtool stores uninstalled libraries. */
#define LT_OBJDIR ".libs/"

/* Name of package */
#define PACKAGE "libwallycore"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT ""

/* Define to the full name of this package. */
#define PACKAGE_NAME "libwallycore"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "libwallycore 1.3.0"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "libwallycore"

/* Define to the home page for this package. */
#define PACKAGE_URL ""

/* Define to the version of this package. */
#define PACKAGE_VERSION "1.3.0"

/* Define to necessary symbol if this constant uses a non-standard name on
   your system. */
/* #undef PTHREAD_CREATE_JOINABLE */

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Version number of package */
#define VERSION "1.3.0"

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most
   significant byte first (like Motorola and SPARC, unlike Intel). */
#if defined AC_APPLE_UNIVERSAL_BUILD
# if defined __BIG_ENDIAN__
#  define WORDS_BIGENDIAN 1
# endif
#else
# ifndef WORDS_BIGENDIAN
/* #  undef WORDS_BIGENDIAN */
# endif
#endif

/* Define for Solaris 2.5.1 so the uint32_t typedef from <sys/synch.h>,
   <pthread.h>, or <semaphore.h> is not used. If the typedef were allowed, the
   #define below would cause a syntax error. */
/* #undef _UINT32_T */

/* Define for Solaris 2.5.1 so the uint64_t typedef from <sys/synch.h>,
   <pthread.h>, or <semaphore.h> is not used. If the typedef were allowed, the
   #define below would cause a syntax error. */
/* #undef _UINT64_T */

/* Define for Solaris 2.5.1 so the uint8_t typedef from <sys/synch.h>,
   <pthread.h>, or <semaphore.h> is not used. If the typedef were allowed, the
   #define below would cause a syntax error. */
/* #undef _UINT8_T */

/* Define to `__inline__' or `__inline' if that's what the C compiler
   calls it, or to nothing if 'inline' is not supported under any name.  */
#ifndef __cplusplus
/* #undef inline */
#endif

/* Define to `unsigned int' if <sys/types.h> does not define. */
/* #undef size_t */

/* Define to the type of an unsigned integer type of width exactly 16 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint16_t */

/* Define to the type of an unsigned integer type of width exactly 32 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint32_t */

/* Define to the type of an unsigned integer type of width exactly 64 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint64_t */

/* Define to the type of an unsigned integer type of width exactly 8 bits if
   such a type exists and the standard includes do not define it. */
/* #undef uint8_t */

#include "ccan_config.h"
#endif /*LIBWALLYCORE_CONFIG_H*/
