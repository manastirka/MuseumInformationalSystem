// Привремени чувар места — прави мотор долази из репоа mis-udzbenik
// (scripts/izgradi-u-mis.sh). Љуска никад не сме да остане празна.
const koren = document.getElementById('udzbenik-app');
if (koren) {
    koren.textContent = '';
    const poruka = document.createElement('p');
    poruka.className = 'udzbenik-ucitavanje';
    poruka.setAttribute('role', 'status');
    poruka.textContent = 'Мотор уџбеника још није изграђен';
    koren.appendChild(poruka);
}
