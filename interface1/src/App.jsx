import React, { useState } from 'react';
import './App.css';

function App() {
  const [busca, setBusca] = useState('');
  const [resultados, setResultados] = useState([]);
  const [carregando, setCarregando] = useState(false);

  const handleBuscar = async () => {
    if (!busca.trim()) return;
    
    setCarregando(true);
    try {
      const resposta = await fetch(`http://localhost:5001/buscar?q=${encodeURIComponent(busca)}`);
      if (!resposta.ok) throw new Error('Erro na resposta');
      const dados = await resposta.json();
      setResultados(dados);
    } catch (error) {
      console.error('Erro:', error);
      setResultados([]);
    } finally {
      setCarregando(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleBuscar();
  };

  return (
    <div>
      <header>
        {/* ... (header permanece igual) */}
      </header>

      <section className="main-section">
        <h1>Empresas de todo <span className="highlight">Brasil</span></h1>
        <div className="search-bar">
          <input
            type="text"
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            onKeyPress={handleKeyPress}  
            placeholder="Busque por CNPJ ou Nome / Cidade"
          />
          <button 
            onClick={handleBuscar} 
            disabled={carregando}
          >
            {carregando ? 'Buscando...' : 'Pesquisar'}
          </button>
          
          {resultados.length > 0 ? (
            <ul className="resultados">
              {resultados.map((item, index) => (
                <li key={index} className="resultado-item">
                  <h3>{item['Nome da empresa']}</h3>
                  <p>CNPJ: {item.CNPJ}</p>
                  <p>CNPJ Completo: {item['CNPJ, CNPJ Completo']}</p>
                </li>
              ))}
            </ul>
          ) : (
            !carregando && <p className="sem-resultados">Nenhum resultado encontrado</p>
          )}
        </div>
      </section>
    </div>
  );
}

export default App;
