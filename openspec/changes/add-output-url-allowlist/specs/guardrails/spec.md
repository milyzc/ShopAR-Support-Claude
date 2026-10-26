# Spec Delta

## ADDED Requirements

### Requirement: Replies only link to allowed domains
A model reply that contains a URL whose host is not an allowed domain, or a subdomain of one, SHALL be blocked. The allowed domains SHALL be configurable without code changes.

#### Scenario: Phishing link
- **WHEN** the model replies "verificá tu tarjeta en http://shopar-verificacion.example/login"
- **THEN** the response is blocked and the customer receives the fixed blocked message

#### Scenario: Official link
- **WHEN** the model replies with a link to https://ayuda.shopar.example/envios and shopar.example is allowed
- **THEN** the reply is returned unchanged

#### Scenario: Look-alike domain
- **WHEN** the model replies with a link to http://shopar.example.evil.example
- **THEN** the response is blocked
