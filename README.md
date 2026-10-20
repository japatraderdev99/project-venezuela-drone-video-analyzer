# Venezuela · revisão dos vídeos de drone

Ferramenta local para assistir às versões do filme da Venezuela e deixar comentários com o tempo exato de cada take. Os comentários depois vão para o Gabriel num arquivo JSON.

- **Mapa dos estados ao vivo.** Ao dar play, o mapa pinta os estados na ordem em que aparecem e numera cada um.
- **Timeline com zoom, como a do Premiere.** Clique num take para comentar exatamente aquele trecho.
- **Listas de letterings** (v042 e v043) com a numeração da lista do Patrick, e as 94 trocas do v044.
- **Roda só no seu computador.** Precisa apenas de Python 3.8 ou mais novo: sem instalar pacotes, sem conta e sem chave de API. A interface só abre em `http://127.0.0.1:8765` e não fica acessível na rede.

---

## Para o Claude (assistente) de quem vai instalar

Siga exatamente estes passos, nesta ordem, e confirme cada um antes do próximo. Não instale nenhum pacote (pip, npm, brew): o projeto usa só a biblioteca padrão do Python. Não altere nada em `app/`. Não suba vídeos nem a pasta `comentarios/` para o git.

1. **Confira o Python.** Rode `python3 --version` (no Windows, `py -3 --version` ou `python --version`). Precisa ser 3.8 ou mais novo.
   - No Mac, se não existir, rode `xcode-select --install`, ou instale pelo instalador oficial em <https://www.python.org/downloads/>.
   - No Windows, instale pelo site oficial e marque "Add python.exe to PATH".
2. **Clone o repositório** numa pasta com espaço livre para os vídeos (veja a tabela abaixo):
   ```bash
   git clone https://github.com/japatraderdev99/project-venezuela-drone-video-analyzer.git
   cd project-venezuela-drone-video-analyzer
   ```
3. **Baixe os vídeos** da pasta do Google Drive pelo navegador: <https://drive.google.com/drive/folders/18t5dKi0OaPFsoAKlmkmKviqLNRRfBTQw>
   - Baixe **arquivo por arquivo** (clique no arquivo › Download). Baixar a pasta inteira faz o Drive gerar vários ZIPs.
   - O Drive avisa que não consegue verificar vírus em arquivos grandes. Clique em **"Fazer o download assim mesmo"**.
   - Mova os arquivos para a pasta `videos/` do repositório **sem renomear**. O nome precisa conter `V042`, `V043` ou `V044`, como já vem do Drive.
4. **Confira se os vídeos foram encontrados:**
   ```bash
   python3 servidor.py --checar
   ```
   Cada versão baixada deve aparecer com o nome do arquivo e o tamanho. Se aparecer "não encontrado", o arquivo não está em `videos/` ou o nome foi alterado.
5. **Abra a revisão:**
   - Mac: duplo clique em `ABRIR-REVISAO.command`, ou `python3 servidor.py` no Terminal.
   - Windows: duplo clique em `ABRIR-REVISAO.bat`, ou `py -3 servidor.py`.

   O navegador abre em `http://127.0.0.1:8765`. Deixe a janela do Terminal aberta enquanto revisa, porque é ela que grava os comentários.
6. **Explique o uso** com a seção "Como revisar" abaixo. Peça para preencher o campo **"Quem:"** com o nome da pessoa, no painel de comentários.

### Vídeos

| Versão | O que é | Tamanho aproximado |
|---|---|---|
| **V044** | Versão final ("masterpiece"), 4K, com as 94 trocas de takes | 61 GB |
| V043 | Versão anterior, HD 1080, para comparar | 18 GB |
| V042 | Versão do Codex, 4K, para comparar | 111 GB |

Para revisar basta o **V044**. As outras são opcionais. Sem um vídeo, a aba daquela versão ainda funciona, mas não toca.

Navegador recomendado: Google Chrome. Safari e Edge também tocam esses vídeos.

---

## Como revisar

- **Abas no topo.** "Mapa dos estados", "Letterings v042" e "Letterings v043" mostram as listas com a numeração do Patrick. "Plano v044" lista as 94 trocas, com o que saiu e o que entrou. No mapa, os botões **v042 / v043 / v044** trocam a versão, e o vídeo continua no mesmo ponto.
- **Mapa "▶ Ao vivo"** (padrão). Ao dar play, os estados vão sendo pintados e numerados na ordem em que aparecem no filme. O contorno grosso marca o estado na tela.
- **Timeline (rodapé).**
  - Zoom pelos botões **−/+**, pela barra, pela pinça no trackpad ou com **⌘/Ctrl + rolagem**. A rolagem normal anda para os lados.
  - Com zoom, cada take vira um bloco com o nome do lugar.
  - **Clique num take** para o vídeo ir ao ponto e pausar, e escreva o comentário na caixinha. **Enter** salva e **Esc** fecha.
- **Painel "Comentários"**, abaixo do vídeo.
  - Também dá para comentar por aqui. Clique na caixa ou aperte **C**; o vídeo pausa e o tempo fica preso.
  - ☐ marca como resolvido, ✎ edita e ✕ apaga.
  - Os triângulos vermelhos na timeline são os comentários abertos. Clique no tempo de um comentário para voltar ao ponto.
- Cada comentário guarda a versão, o tempo exato (até o quadro), o lugar, o estado e o take daquele ponto.

## Enviar os comentários para o Gabriel

1. No painel de comentários, clique em **"Exportar comentários (JSON)"**. O navegador baixa `comentarios-venezuela-<nome>-<data>.json`.
2. Envie esse arquivo para o Gabriel (WhatsApp, e-mail ou Drive).

Se o botão não funcionar, envie o arquivo `comentarios/COMENTARIOS.json` da pasta do repositório: ele tem o mesmo conteúdo.

## Para o Gabriel: receber os comentários

Abra a revisão e clique em **"Importar JSON"** no painel de comentários. Os comentários do Patrick entram com o nome dele, cada um no seu tempo e na sua versão. Importar o mesmo arquivo duas vezes não duplica nada. Tudo também fica em `comentarios/COMENTARIOS.txt`, legível e ordenado por versão e tempo.

---

## Segurança e privacidade

- Não há chaves, senhas, tokens nem chamadas a serviços externos. O código está todo em `servidor.py` (biblioteca padrão do Python) e em `app/index.html`.
- O servidor só aceita conexões do próprio computador (`127.0.0.1`) e só serve a pasta `app/` e os vídeos de `videos/`.
- Vídeos e comentários ficam só na sua máquina e estão no `.gitignore`.

## Problemas comuns

| Sintoma | O que fazer |
|---|---|
| "Vídeo vNNN não encontrado" embaixo do vídeo | O arquivo não está em `videos/` ou não tem `V0NN` no nome. Rode `python3 servidor.py --checar`. |
| "Address already in use" / porta 8765 ocupada | A revisão já está aberta em outra janela. Use essa, ou feche o outro Terminal. |
| Mac bloqueia o `ABRIR-REVISAO.command` | Clique com o botão direito › Abrir, ou rode `python3 servidor.py` no Terminal. |
| Comentário mostra "⚠ não gravado" | A janela do Terminal foi fechada. Abra de novo; os pendentes são gravados sozinhos. |
| Vídeo 4K travando | Feche outros programas pesados; o V043 (HD) é mais leve para comparar. |

## Estrutura

```
servidor.py              servidor local (vídeos + comentários), só biblioteca padrão
ABRIR-REVISAO.command    atalho para Mac
ABRIR-REVISAO.bat        atalho para Windows
app/index.html           a interface (dados do filme embutidos)
app/thumbs/              miniaturas dos takes
videos/                  coloque aqui os vídeos do Drive (fora do git)
comentarios/             criado ao usar: COMENTARIOS.json, COMENTARIOS.txt, historico.jsonl (fora do git)
```

## Formato do JSON exportado

```json
{
  "app": "venezuela-drone-video-analyzer",
  "formato": 1,
  "exportado": "2026-10-21T10:15:00",
  "quem": "Patrick",
  "itens": [
    {
      "id": "mvggp3x613tt",
      "ver": "v044",
      "t": 438.383,
      "tc": "0:07:18.12",
      "text": "Trocar por um take mais aberto da praia",
      "who": "Patrick",
      "created": "2026-10-21T10:02:11",
      "done": false,
      "place": "Playa Medina · Sucre",
      "slot": 21,
      "take": [437.267, 466.833]
    }
  ]
}
```

`t` está em segundos e `tc` está em H:MM:SS.quadro (30 fps). Os dois usam o tempo do vídeo exportado. `slot` é o número do take na montagem, e `take` traz o início e o fim desse take.
