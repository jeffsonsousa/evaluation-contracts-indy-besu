'use strict';

const OperationBase = require('./utils/operation-base');

class createRevocationRegistry extends OperationBase {
    constructor() {
        super();
    }
    
    async submitTransaction() {
        
        const revRegistry = ["1.0.0", "revReg123", "CL", "did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN/anoncreds/v0/CLAIM_DEF/did:indy2:indy_besu:MRDxoJ2Mz3ZuyqaqsjVTdN/anoncreds/v0/SCHEMA/BasicIdentity/1.0.0/BasicIdentity233", "test-tag", "value123", "did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN"]

        // const revRegistry =  ["1.0.0", "revReg123", "CL", "did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN/anoncreds/v0/CLAIM_DEF/did:indy2:indy_besu:MRDxoJ2Mz3ZuyqaqsjVTdN/anoncreds/v0/SCHEMA/BasicIdentity/1.0.0/BasicIdentity233", "test-tag", "value123", "did:indy2:indy_besu:MRDxoJ2Mz4ZuyqaqsjVTdN"]

        await this.sutAdapter.sendRequests(this.createConnectorRequest('createRevocationRegistry', revRegistry));
    }
}

function createWorkloadModule() {
    return new createRevocationRegistry();
}

module.exports.createWorkloadModule = createWorkloadModule;