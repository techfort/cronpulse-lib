const axios = require('axios');

class CronPulse {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://api.cronpulse.com'; // Replace with your API URL
    }

    async createMonitor(name, interval, email, expiresAt) {
        const response = await axios.post(`${this.baseUrl}/monitors`, {
            name, interval, email, expires_at: expiresAt.toISOString()
        }, { headers: { Authorization: `Bearer ${this.apiKey}` } });
        return new Monitor(response.data.id, this.apiKey);
    }
}

class Monitor {
    constructor(monitorId, apiKey) {
        this.monitorId = monitorId;
        this.apiKey = apiKey;
    }

    async ping() {
        await axios.post(`${this.baseUrl}/monitors/${this.monitorId}/ping`, {}, { headers: { Authorization: `Bearer ${this.apiKey}` } });
    }

    async delete() {
        await axios.delete(`${this.baseUrl}/monitors/${this.monitorId}`, { headers: { Authorization: `Bearer ${this.apiKey}` } });
    }
}

module.exports = { CronPulse };
