
import aea
import click


def encrypt(
	input_file, output_file, profile, algorithm, block_size, padding_size,
	sign_pub_file, sign_pub_value,
	sign_priv_file, sign_priv_value,
	signature_key,
	key_file, key_value, key_gen,
	password_file, password_value, password_gen,
	recipient_pub_file, recipient_pub_value

):
	has_key = key_file or key_value or key_gen
	has_signature = sign_pub_file or sign_pub_value or sign_priv_file or sign_priv_value or signature_key
	has_password = password_file or password_value or password_gen
	has_recipient = recipient_pub_file or recipient_pub_value

	if has_password and (has_key or has_signature or has_recipient):
		raise click.UsageError("Invalid options for profile")
	if has_recipient and has_key:
		raise click.UsageError("Invalid options for profile")
	
	expected_profile = None
	if has_key and not has_signature:
		expected_profile = aea.ProfileType.AESCTR
	elif has_key and has_signature:
		expected_profile = aea.ProfileType.AESCTR_ECDSA
	elif has_recipient and not has_signature:
		expected_profile = aea.ProfileType.ECDHE
	elif has_recipient and has_signature:
		expected_profile = aea.ProfileType.ECDHE_ECDSA
	elif has_password:
		expected_profile = aea.ProfileType.SCRYPT
	elif has_signature:
		expected_profile = aea.ProfileType.ECDSA
	
	if profile is None:
		profile = expected_profile
	elif profile != expected_profile:
		raise click.UsageError("Invalid options for profile")
	
	...

def decrypt(input_file, output_file):
	...

def sign(output_file):
	pass

def append(input_file, output_file):
	pass

def id(input_file):
	pass

def parse_profile(ctx, param, value):
	# When no profile is provided, it is determined from
	# the other arguments.
	if value is None:
		return
	
	profiles = [
		"hkdf_sha256_hmac__none__ecdsa_p256",
		"hkdf_sha256_aesctr_hmac__symmetric__none",
		"hkdf_sha256_aesctr_hmac__symmetric__ecdsa_p256",
		"hkdf_sha256_aesctr_hmac__ecdhe_p256__none",
		"hkdf_sha256_aesctr_hmac__ecdhe_p256__ecdsa_p256",
		"hkdf_sha256_aesctr_hmac__scrypt__none"
	]
	if value in profiles:
		return profiles.index(value)
	if value.isdecimal() and 0 <= int(value) <= 5:
		return int(value)
	raise click.BadParameter(value)

def parse_size(ctx, param, value):
	shift = 0
	number = 0

	units = {
		"b": 0,
		"k": 10,
		"m": 20,
		"g": 30
	}
	if value and value[-1] in units:
		shift = units[value[-1]]
		number = value[:-1]
	else:
		number = value
	
	if not number.isdecimal():
		raise click.BadParameter(value)
	
	return int(number) << shift

def parse_padding_size(ctx, param, value):
	if value is None:
		return None
	
	if value == "none": return 0
	elif value == "adaptive": return 1
	else:
		size = parse_size(ctx, param, value)
		if size != 0 and size < 16:
			raise click.BadParameter(value)
		return size

profile_help = """
\b
Archive profile, one of (index and string are both valid):
0: hkdf_sha256_hmac__none__ecdsa_p256
1: hkdf_sha256_aesctr_hmac__symmetric__none
2: hkdf_sha256_aesctr_hmac__symmetric__ecdsa_p256
3: hkdf_sha256_aesctr_hmac__ecdhe_p256__none
4: hkdf_sha256_aesctr_hmac__ecdhe_p256__ecdsa_p256
5: hkdf_sha256_aesctr_hmac__scrypt__none
"""

verbose_option = click.Option(
	["-v", "verbosity"],
	help="Increase verbosity, default is silent",
	count=True
)

input_option = click.Option(
	["-i", "input_file"],
	metavar="input_file",
	help="Input file. Default is stdin",
	type=click.Path(exists=True, dir_okay=False, allow_dash=True),
	default="-"
)

output_option = click.Option(
	["-o", "output_file"],
	metavar="output_file",
	help="Output file. Default is stdin",
	type=click.Path(dir_okay=False, writable=True, allow_dash=True),
	default="-"
)

profile_option = click.Option(
	["-profile"],
	metavar="p",
	help=profile_help,
	callback=parse_profile
)

algorithm_option = click.Option(
	["-a", "algorithm"],
	metavar="algorithm",
	help="Compression algorithm, one of lzfse, lzma, zlib, lz4, lzbitmap, none (no compression), default is lzfse",
	type=click.Choice(["lzfse", "lzma", "zlib", "lz4", "lzbitmap", "copy", "raw", "none"]),
)

block_size_option = click.Option(
	["-b", "block_size"],
	metavar="block_size",
	help="Compression and encryption block size, units are b=1 byte, k=2^10 bytes, m=2^20 bytes, q=2^30 bytes, default value is 1m",
	callback=parse_size,
	default=0x1000000
)

range_offset_option = click.Option(
	["-range-offset"],
	metavar="offset",
	help="Offset (bytes in uncompressed data) of range to decrypt",
	callback=parse_size
)

range_size_option = click.Option(
	["-range-size"],
	metavar="size",
	help="Size (bytes in uncompressed data) of range to decrypt",
	callback=parse_size
)

padding_size_option = click.Option(
	["-padding", "padding_size"],
	metavar="padding_size",
	help="Padding size, units are b=1 byte, k=2^10 bytes, m=2^20 bytes, g=2^30 bytes, default is defined for each profile. Can also be 'none' or 0 for no padding, or 'adaptive' for adaptive Padmé padding size. Numerical values other than 0 must be >= 16.",
	callback=parse_padding_size
)

checksum_option = click.Option(
	["-checksum"],
	metavar="digest",
	help="Checksum mode, one of none, murmur64, sha256, default is defined for each profile",
	type=click.Choice(["none", "murmur64", "sha256"])
)

key_file_option = click.Option(
	["-key", "key_file"],
	metavar="key_file",
	help="File providing key for symmetric encryption mode",
	type=click.Path(dir_okay=False)
)

key_value_option = click.Option(
	["-key-value"],
	metavar="key",
	help="Key for symmetric encryption mode (hex or base64 encoded)"
)

key_gen_option = click.Option(
	["-key-gen"],
	help="When encrypting using the symmetric encryption mode. Generate a random high entropy key, and store it in `key_file`.",
	is_flag=True
)

password_file_option = click.Option(
	["-password", "password_file"],
	metavar="password_file",
	help="File providing password for password encryption mode",
	type=click.Path(dir_okay=False)
)

password_value_option = click.Option(
	["password-value"],
	metavar="password",
	help="Password for password encryption mode"
)

password_gen_option = click.Option(
	["-password-gen"],
	help="When encrypting using the password encryption mode. Generate a random password and store it in `password_file`",
	is_flag=True
)

auth_data_key_option = click.Option(
	["-auth-data-key"],
	metavar="string",
	help="Specifies the key to use for the next `-auth-data file` or `-auth-data-value data` option. If this option is given, the auth data blob in the archive will use the key->value format, and this option must be given before each `-auth-data file` or `-auth-data-value data` option",
	multiple=True,
	callback=
)

auth_data_file_option = click.Option(
	["-auth-data"],
	metavar="file",
	help="Insert the contents of a file as authentication data in the document prologue. This option can be specified multiple times, and data will be added at the end. If this option is specified after a -auth-data-key string, then the file contents will be stored under the key, and auth data will use the key->value format",
	type=click.Path(exists=True, dir_okay=False),
	multiple=True
)

auth_data_value_option = click.Option(
	["-auth-data-value"],
	metavar="data",
	help="Insert the contents of data (hex or base64 encoded) as authentication data in the document prologue. This option can be specified multiple times, and data will be added at the end. If this option is specified after a `-auth-data-key string`, then the data will be stored under the key, and auth data will use the key->value format",
	multiple=True
)

sign_pub_file_option = click.Option(
	["-sign-pub", "sign_pub_file"],
	metavar="key_file",
	help="Sender's public key used to verify signature, and encrypt the document",
	type=click.Path(exists=True, dir_okay=False)
)

sign_pub_value_option = click.Option(
	["-sign-pub-value"],
	metavar="key",
	help="Sender's public key used to verify signature, and encrypt the document (hex or base64 X9.63 encoded)"
)

sign_priv_file_option = click.Option(
	["-sign-priv", "sign_priv_file"],
	metavar="key_file",
	help="Sender's private key used to sign the document",
	type=click.Path(exists=True, dir_okay=False)
)

sign_priv_value_option = click.Option(
	["-sign-priv-value"],
	metavar="key",
	help="Sender's private key used to sign the document (hex or base64 X9.63 encoded)"
)

recipient_pub_file_option = click.Option(
	["-recipient-pub", "recipient_pub_file"],
	metavar="key_file",
	help="Recipient's public key used to encrypt the document",
	type=click.Path(exists=True, dir_okay=False)
)

recipient_pub_value_option = click.Option(
	["-recipient-pub-value"],
	metavar="key",
	help="Recipient's public key used to encrypt the document (hex or base64 X9.63 encoded)"
)

recipient_priv_file_option = click.Option(
	["-recipient-priv", "recipient_priv_file"],
	metavar="key_file",
	help="Recipient's private key used to decrypt the document",
	type=click.Path(exists=True, dir_okay=False)
)

recipient_priv_value_option = click.Option(
	["-recipient-priv-value"],
	metavar="key",
	help="Recipient's private key used to decrypt the document (hex or base64 X9.63 encoded)"
)

main_key_option = click.Option(
	["-main-key"],
	metavar="key_file",
	help="If provided with 'encrypt', store the document main key in key_file. Required with -append to re-open the document for the `ecdhe` profiles",
	type=click.Path(exists=True, dir_okay=False)
)

signature_key_option = click.Option(
	["-signature-key"],
	metavar="key_file",
	help="If provided with 'encrypt' or 'append', store the signature encryption key in key_file. Required with -sign to sign the document",
	type=click.Path(exists=True, dir_okay=False)
)

encrypt_command = click.Command(
	"encrypt", callback=encrypt,
	short_help="Create a new AEA archive",
	help="Create a new encrypted archive `output_file` from the data in `input_file`",
	params=[
		input_option, output_option, profile_option, algorithm_option,
		block_size_option, padding_size_option,
		sign_pub_file_option, sign_pub_value_option,
		sign_priv_file_option, sign_priv_value_option,
		signature_key_option,
		key_file_option, key_value_option, key_gen_option,
		password_file_option, password_value_option, password_gen_option,
		recipient_pub_file_option, recipient_pub_value_option
	],
	no_args_is_help=True,
)

decrypt_command = click.Command(
	"decrypt", callback=decrypt,
	short_help="Decrypt an AEA archive",
	help="Decrypt the contents of encrypted archive `input_file` to `output_file`",
	params=[input_option, output_option, range_offset_option],
	no_args_is_help=True
)

sign_command = click.Command(
	"sign", callback=sign,
	short_help="Sign an AEA archive",
	help="Sign an existing encrypted archive `output_file`",
	params=[output_option],
	no_args_is_help=True
)

append_command = click.Command(
	"append", callback=append,
	short_help="Append data to an existing AEA archive",
	help="Append the contents of `input_file` to an existing encrypted archive `output_file`",
	params=[input_option, output_option],
	no_args_is_help=True
)

id_command = click.Command(
	"id", callback=id,
	short_help="Identify an AEA archive",
	help="Print archive identifier for `input_file`",
	params=[input_option],
	no_args_is_help=True
)

context_settings = {
	"help_option_names": ["-h", "--help"]
}

cli = click.Group(options_metavar=None, context_settings=context_settings)
cli.add_command(encrypt_command)
cli.add_command(decrypt_command)
cli.add_command(sign_command)
cli.add_command(append_command)
cli.add_command(id_command)
