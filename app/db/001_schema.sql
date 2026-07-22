CREATE TABLE IF NOT EXISTS pets (
    id text PRIMARY KEY,
    name text NOT NULL,
    species text NOT NULL,
    status text NOT NULL CHECK (status IN ('available', 'pending', 'adopted')),
    adoption_fee_cents integer NOT NULL CHECK (adoption_fee_cents >= 0)
);

CREATE TABLE IF NOT EXISTS adoptions (
    id bigserial PRIMARY KEY,
    pet_id text NOT NULL REFERENCES pets(id),
    adopter_email text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (pet_id)
);

INSERT INTO pets (id, name, species, status, adoption_fee_cents) VALUES
    ('pet-100', 'Mochi', 'cat', 'available', 7500),
    ('pet-101', 'Scout', 'dog', 'available', 12500),
    ('pet-102', 'Pip', 'rabbit', 'available', 4500),
    ('pet-103', 'Nova', 'dog', 'pending', 11000)
ON CONFLICT (id) DO NOTHING;
