const { execSync } = require('child_process');
const express = require('express');
const logS = require('log-symbols');
const os = require('os');
const path = require('path');
const fs = require('fs');

app = express()
const SAVE_TO = path.join(os.homedir(), 'INFOS_EXTRAIDAS');
if (!fs.existsSync(SAVE_TO)) fs.mkdir(SAVE_TO);

app.get('/*', (req,res) => {
    const d = req.query;
    // transforma em CSV
    d.NOME = execSync(`echo ${d.NOME} | base64 -d`).toString('utf8').replace(/(\r\n|\n|\r)/gm, "");;
    d.CPF = execSync(`echo ${d.CPF} | base64 -d`).toString('utf8').replace(/(\r\n|\n|\r)/gm, "");;
    d.NASCIMENTO = execSync(`echo ${d.NASCIMENTO} | base64 -d`).toString('utf8').replace(/(\r\n|\n|\r)/gm, "");;
    d.TEL1 = execSync(`echo ${d.TEL1} | base64 -d`).toString('utf8').replace(/(\r\n|\n|\r)/gm, "");;
    d.TEL2 = execSync(`echo ${d.TEL2} | base64 -d`).toString('utf8').replace(/(\r\n|\n|\r)/gm, "");;
    d.TEL3 = execSync(`echo ${d.TEL3} | base64 -d`).toString('utf8').replace(/(\r\n|\n|\r)/gm, "");;
    d.TEL4 = execSync(`echo ${d.TEL4} | base64 -d`).toString('utf8').replace(/(\r\n|\n|\r)/gm, "");;

    const csv = `"${d.NOME}","${d.CPF}","${d.NASCIMENTO}","${(d.TEL1)?d.TEL1:''}","${(d.TEL2)?d.TEL2:''}","${(d.TEL3)?d.TEL3:''}","${(d.TEL4)?d.TEL4:''}"`;
    console.info(logS.success, "CSV RECEBIDO: ", csv);
    
    const saveIn = path.join(SAVE_TO, d.concatTo);
    fs.appendFile(saveIn, csv.concat('\n'), (err) => {
        if (err) {
            console.error(`${logS.error} Erro ao salvar csv motivo: ${err.message}`);
        }
    });

    res.sendStatus(200);
});

app.listen({
    port: 38610,
    host: "127.0.0.1"
},()=> {
    console.info(logS.info, "\n Aguardando string csv em 127.0.0.1:38610...");
})