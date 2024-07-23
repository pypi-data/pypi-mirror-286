# ejabberd extauth script for OIDC Password Grant Flow

This script enables the use of OIDC providers for password login in ejabberd.
It uses the [Password Grant](https://oauth.net/2/grant-types/password/), which
is considered legacy. However, with ejabberd [lacking proper OIDC support](https://github.com/processone/ejabberd/issues/3437),
it is a viable work-around.

## Installation

It is best to install the script using `pip` until it gets available in distributions:

```shell
sudo pip install --break-system-packages ejhabberd-extauth-oidc-password
```

This makes the script available at `/usr/local/bin/ejabberd_extauth_oidc_password`.

## Configuration

### Configuring the script

The script needs the following information about the OIDC provider:

* Issuer URL
* Token URL
* Client ID
* Client secret

Then, the script can be configured in `/etc/ejabberd/extauth/oidc_password.yml`:

```yaml
handler:
  test.example.com:  # one block per XMPP server domain
    issuer: https://idp.example.com
    token_url: https://idp.example.com/oauth/token/
    client_id: myclient_abcd
    client_secret: top_secret
```

### Configuring ejabberd

For ejabberd, follow the instructions for [configuring external authentication](https://docs.ejabberd.im/admin/configuration/authentication/#external-script).
Set `extauth_program` to `/usr/local/bin/ejabberd_extauth_oidc_password`.
