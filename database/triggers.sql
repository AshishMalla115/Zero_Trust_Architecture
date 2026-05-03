-- 1. REVOKE delete/update on append-only tables from app user
REVOKE UPDATE, DELETE ON risk_event_log FROM zt_app;
REVOKE UPDATE, DELETE ON admin_audit_log FROM zt_app;

-- 2. Trigger: only one active ML model at a time
CREATE OR REPLACE FUNCTION enforce_single_active_model()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_active = TRUE THEN
        UPDATE ml_model_versions SET is_active = FALSE
        WHERE id != NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_single_active_model
AFTER INSERT OR UPDATE ON ml_model_versions
FOR EACH ROW EXECUTE FUNCTION enforce_single_active_model();

-- 3. HMAC verification function (Ashish writes HMAC on insert; this checks it)
CREATE OR REPLACE FUNCTION verify_risk_event_hmacs()
RETURNS TABLE(bad_row_id INT, stored_hmac TEXT) AS $$
BEGIN
    -- Flag rows where hmac is null (should never be null after week 6)
    RETURN QUERY
    SELECT id, row_hmac::TEXT
    FROM risk_event_log
    WHERE row_hmac IS NULL;
    -- Full cryptographic check is done at application level since
    -- pgcrypto would need the HMAC key, which stays in the backend
END;
$$ LANGUAGE plpgsql;

-- 4. Index for dashboard real-time queries
CREATE INDEX idx_risk_event_session_time 
    ON risk_event_log(session_id, created_at DESC);

CREATE INDEX idx_risk_event_user_time 
    ON risk_event_log(user_id, created_at DESC);

CREATE INDEX idx_active_sessions_risk 
    ON active_sessions(current_risk_score DESC) WHERE is_active = TRUE;

CREATE INDEX idx_alerts_unresolved 
    ON alerts(is_resolved, created_at DESC);