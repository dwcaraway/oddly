Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

exec { 'apt-get update':
  command => 'apt-get update',
  timeout => 60,
  tries => 3
}

$sysPackages = [ "build-essential", 'git' ]
package { $sysPackages:
  ensure => "installed",
  require => Exec['apt-get update'],
}

apache::module {'wsgi':}

apache::vhost { 'default':
  docroot             => '/vagrant/wsgi',
  server_name         => false,
  priority            => '',
  template            => 'apache/virtualhost/vhost.conf.erb',
}

include apache
