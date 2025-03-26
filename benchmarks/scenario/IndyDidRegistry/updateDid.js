'use strict';

const OperationBase = require('./utils/operation-base');

class UpdateDid extends OperationBase {
    constructor() {
        super();
    }
    
    async submitTransaction() {
        
        const document = [[],"did:indy2:indy_besu:MRDxoJ2Mz3ZuyqaqsjVTdN",[],[["did:indy2:indy_besu:RQDxoJ2Mz3WuyqaqsjVTdN#KEY-1","Ed25519VerificationKey2018", "did:indy2:testnet:MUDA_N22WedHLJdFf4yMaDXdhJcL98","MUDA_HAFkhqbPbor781QCMfNvr6oQTTixK9U7gZmDV7pszTHp",""]],[["did:indy2:indy_besu:RQDxoJ2Mz3WuyqaqsjVTdN#KEY-1",["1","1","1","1","1"]]],[],[],[],[],[],[]]
        await this.sutAdapter.sendRequests(this.createConnectorRequest('updateDid', document));
    }
}

function createWorkloadModule() {
    return new UpdateDid();
}

module.exports.createWorkloadModule = createWorkloadModule; 