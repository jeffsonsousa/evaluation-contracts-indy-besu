'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');

const SupportedConnectors = ['ethereum'];

class OperationBase extends WorkloadModuleBase {
    constructor() {
        super();
    }

    async initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext) {
        await super.initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext);

        this.assertConnectorType();
        this.assertSetting('schema');

        this.schema = this.roundArguments.schema;
    }

    assertConnectorType() {
        this.connectorType = this.sutAdapter.getType();
        if (!SupportedConnectors.includes(this.connectorType)) {
            throw new Error(`Connector type ${this.connectorType} is not supported by the benchmark`);
        }
    }

    assertSetting(settingName) {
        if (!this.roundArguments.hasOwnProperty(settingName)) {
            throw new Error(`Simple workload error: module setting "${settingName}" is missing from the benchmark configuration file`);
        }
    }

    createConnectorRequest(operation, args) {
        switch (this.connectorType) {
            case 'ethereum':
                return this._createEthereumConnectorRequest(operation, args);
            default:
                throw new Error(`Connector type ${this.connectorType} is not supported by the benchmark`);
        }
    }

    _createEthereumConnectorRequest(operation, args) {
        const query = operation === 'query';
        return {
            contract: 'SchemaRegistry',
            verb: operation,
            args: [args],
            readOnly: query
        };
    }
}

module.exports = OperationBase;