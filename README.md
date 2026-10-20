# Venezuela · revisão dos vídeos de drone

Ferramenta local para assistir às versões do filme da Venezuela e comentar com o tempo exato de cada take. Ela já vem com os **comentários do Guilherme** carregados. No final, os comentários vão de volta para o Guilherme num arquivo JSON.

- **Comentários com tempo exato.** Dá para concordar (👍), responder (↩) ou escrever um comentário novo. Quando o vídeo passa por um comentário, ele aparece por cima da imagem.
- **Mapa dos estados ao vivo.** Ao dar play, os estados acendem e ganham um número na ordem em que aparecem.
- **Timeline com zoom, como a do Premiere.** Clique num take para comentar nele e aperte a rodinha do mouse para arrastar.
- **Tutorial na tela** na primeira vez que abre. Dá para pular, e o botão "Como usar" reabre.
- **Roda só no seu computador.** Precisa apenas de Python 3.8 ou mais novo: sem instalar pacotes, sem conta e sem chave de API. A interface só abre em `http://127.0.0.1:8765` e não fica acessível na rede.

---

## Para o Claude (assistente) de quem vai instalar

Siga exatamente estes passos, nesta ordem, e confirme cada um antes do próximo. Não instale nenhum pacote (pip, npm, brew): o projeto usa só a biblioteca padrão do Python. Não altere nada em `app/`. Não suba vídeos nem a pasta `comentarios/` para o git.

1. **Confira o Python.** Rode `python3 --version` (no Windows, `py -3 --version` ou `python --version`). Precisa ser 3.8 ou mais novo.
   - No Mac, se não existir, rode `xcode-select --install`, ou instale pelo instalador oficial em <https://www.python.org/downloads/>.
   - No Windows, instale pelo site oficial e marque "Add python.exe to PATH".
2. **Clone o repositório** numa pasta de um disco com espaço livre para os vídeos (veja a tabela abaixo):
   ```bash
   git clone https://github.com/japatraderdev99/project-venezuela-drone-video-analyzer.git
   cd project-venezuela-drone-video-analyzer
   ```
3. **Baixe os vídeos** da pasta do Google Drive pelo navegador: <https://drive.google.com/drive/folders/18t5dKi0OaPFsoAKlmkmKviqLNRRfBTQw>
   - Baixe **arquivo por arquivo** (clique com o botão direito no arquivo › Fazer download). Baixar a pasta inteira faz o Drive gerar vários ZIPs.
   - O Drive avisa que não consegue verificar vírus em arquivos grandes. Clique em **"Fazer o download assim mesmo"**.
   - Mova os arquivos para a pasta `videos/` do repositório **sem renomear**.
4. **Confira os vídeos:**
   ```bash
   python3 servidor.py --checar
   ```
   Cada vídeo baixado deve aparecer com o nome e o tamanho da tabela abaixo. Se o tamanho for menor, o download não terminou.
5. **Abra a revisão:**
   - Mac: duplo clique em `ABRIR-REVISAO.command`, ou `python3 servidor.py` no Terminal.
   - Windows: duplo clique em `ABRIR-REVISAO.bat`, ou `py -3 servidor.py`.

   O navegador abre em `http://127.0.0.1:8765` e mostra o tutorial. Deixe a janela do Terminal aberta enquanto revisa, porque é ela que grava os comentários. Na primeira vez, o Terminal mostra "21 comentários iniciais carregados".
6. **Peça para a pessoa preencher "Você:"** com o nome dela, no painel de comentários. Sem nome, a interface não deixa comentar, concordar nem responder.

### Vídeos

| Arquivo no Drive | O que é | Tamanho |
|---|---|---|
| `VENEZUELA_V044_MASTERPIECE_UHD30_H264_55Mbps_YOUTUBE.mp4` | **Versão final, 4K. É a que tem os comentários** | 61,4 GB (61.375.955.099 bytes) |
| `VENEZUELA_V043_CURADORIA_CLAUDE_REVISAO_HD1080.mp4` | Versão anterior, HD 1080, para comparar | 18,1 GB (18.091.095.000 bytes) |

Para revisar basta o **V044**; o V043 é opcional. A aba v042 aparece na interface, mas o vídeo dela não está no Drive. Sem o vídeo, a aba de uma versão continua funcionando, só não toca.

Navegador recomendado: Google Chrome. Safari e Edge também tocam esses vídeos.

---

## Como revisar

| Ação | Como |
|---|---|
| Play / pausa | **Barra de espaço** |
| Voltar / avançar 5 s | Setas **← →** |
| Comentar no ponto atual | Tecla **C**, ou clique na caixa de comentários. O vídeo pausa e o tempo fica marcado; **Enter** salva. |
| Comentar num take | Clique no bloco do take na timeline, escreva e dê **Enter** (**Esc** fecha). |
| Zoom na timeline | **Pinça** no trackpad, **⌘/Ctrl + rolagem** ou os botões −/+ |
| Andar pela timeline | **Aperte a rodinha do mouse e arraste**, ou role para os lados |
| Concordar / responder | **👍 Concordo** e **↩ Responder** em cada comentário |
| Ir ao ponto de um comentário | Clique no tempo azul do comentário, ou no triângulo vermelho na timeline |
| Trocar de versão | Botões **v042 / v043 / v044** no mapa. O vídeo continua no mesmo ponto. |
| Ver o tutorial de novo | Botão **Como usar**, no canto superior direito |

Mais detalhes da interface:
- O comentário do ponto atual aparece por cima do vídeo e fica destacado na lista.
- A borda vermelha marca os comentários abertos; marque "resolvido" quando um estiver tratado.
- As abas "Letterings v042/v043" mostram as listas com a numeração do Patrick. "Plano v044" mostra as 94 trocas de takes, com o que saiu e o que entrou.

## Enviar os comentários para o Guilherme

1. No painel de comentários, clique em **"Exportar comentários (JSON)"**. O navegador baixa `comentarios-venezuela-<nome>-<data>.json`.
2. Envie esse arquivo para o Guilherme (WhatsApp, e-mail ou Drive).

Se o botão não funcionar, envie o arquivo `comentarios/COMENTARIOS.json` da pasta do repositório: ele tem o mesmo conteúdo.

## Para o Guilherme: receber os comentários

Clique em **"Importar JSON"** no painel de comentários. As respostas e as concordâncias do Patrick se juntam aos comentários que você já tem, e os comentários novos dele entram com o nome dele. Importar o mesmo arquivo de novo não duplica nada. Tudo também fica em `comentarios/COMENTARIOS.txt`, ordenado por versão e tempo.

Para mandar comentários novos para o Patrick:
- **Pelo JSON:** exporte e mande o arquivo, e ele importa do mesmo jeito.
- **Pelo git:** coloque o arquivo exportado em `app/seed/` e faça o push. Depois de um `git pull`, os comentários novos entram uma única vez; o que ele apagou não volta.

---

## Segurança e privacidade

- Não há chaves, senhas, tokens nem chamadas a serviços externos. O código está todo em `servidor.py` (biblioteca padrão do Python) e em `app/index.html`.
- O servidor só aceita conexões do próprio computador (`127.0.0.1`) e só serve a pasta `app/` e os vídeos de `videos/`.
- Vídeos e comentários ficam só na sua máquina e estão no `.gitignore`. Os únicos comentários no repositório são os iniciais, em `app/seed/`.

## Problemas comuns

| Sintoma | O que fazer |
|---|---|
| "Vídeo v044 não encontrado" embaixo do vídeo | O arquivo não está em `videos/` ou foi renomeado. Rode `python3 servidor.py --checar`. |
| "Address already in use" / porta 8765 ocupada | A revisão já está aberta em outra janela. Use essa, ou rode `python3 servidor.py --porta 8770`. |
| Mac bloqueia o `ABRIR-REVISAO.command` | Clique com o botão direito › Abrir, ou rode `python3 servidor.py` no Terminal. |
| Comentário mostra "⚠ não gravado" | A janela do Terminal foi fechada. Abra de novo; os pendentes são gravados sozinhos. |
| Concordo, Responder ou comentar não fazem nada | Preencha o campo **"Você:"** com o seu nome. |
| Vídeo 4K travando | Feche outros programas pesados; o V043 (HD) é mais leve. |

## Estrutura

```
servidor.py              servidor local (vídeos + comentários), só biblioteca padrão
ABRIR-REVISAO.command    atalho para Mac
ABRIR-REVISAO.bat        atalho para Windows
app/index.html           a interface (dados do filme embutidos)
app/thumbs/              miniaturas dos takes
app/seed/                comentários iniciais (do Guilherme), carregados uma vez
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
      "id": "mvgi5zopzeem",
      "ver": "v044",
      "t": 158.707,
      "tc": "0:02:38.21",
      "text": "tremidinha no começo do video, talvez iniciar mais tarde o take",
      "who": "Guilherme",
      "created": "2026-10-20T06:50:33",
      "done": false,
      "place": "Laguna de Mucubají · Mérida",
      "slot": 8,
      "take": [152.333, 181.167],
      "concordo": ["Patrick"],
      "respostas": [
        {"id": "mvh01abcd", "who": "Patrick", "text": "Ok, começa 2 s depois", "created": "2026-10-21T10:03:40"}
      ],
      "updated": "2026-10-21T10:03:40"
    }
  ]
}
```

`t` está em segundos e `tc` em H:MM:SS.quadro (30 fps). Os dois usam o tempo do vídeo exportado. `slot` é o número do take na montagem, `take` traz o início e o fim desse take, e `concordo` lista quem concordou.
