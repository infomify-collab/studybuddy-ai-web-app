"""A Python web interface. Streamlit runs the Python server for us."""
from pathlib import Path
import streamlit as st
from study_ai import generate_pack, prepare_notes, get_api_key, to_markdown, StudyError, MAX_NOTES, MODEL

st.set_page_config(page_title='StudyBuddy | CodeWithHimi', page_icon='📚', layout='wide')
st.caption('CODE WITH HIMI / BUILD YOUR FIRST AI WEB APP')
st.title('Your notes. A clearer way to study.')
st.write('Turn a small set of notes into a summary, flashcards and a quiz — then check the answers against your source.')

with st.sidebar:
    st.subheader('StudyBuddy')
    st.write('Python + Streamlit + Gemini')
    st.caption(f'Model: {MODEL}')
    try:
        connected = bool(get_api_key())
    except StudyError:
        connected = False
    if connected:
        st.success('Local key configured')
    else:
        st.info('Run python setup_key.py to configure Gemini.')
    st.caption('Generation sends the notes to Google Gemini. Use public or permitted material. API usage may cost money depending on your project tier.')
    st.caption('One submitted form = one request. Changing quiz answers does not call Gemini.')

sample = (Path(__file__).parent / 'examples' / 'ai_notes.txt').read_text()
with st.form('study_input'):
    notes = st.text_area('Study notes', value=sample, height=210, max_chars=MAX_NOTES)
    language = st.selectbox('Output language', ['English', 'Hinglish'])
    approved = st.checkbox('These notes are OK to send to Gemini.')
    submitted = st.form_submit_button('Create my study pack', type='primary')

if submitted:
    st.session_state.pop('study_pack', None)
    st.session_state.pop('checked_quiz', None)
    if not approved:
        st.warning('Confirm that these notes are OK to send before generating.')
    else:
        try:
            with st.spinner('Gemini is preparing your study pack…'):
                pack, receipt = generate_pack(notes, language)
            st.session_state['study_pack'] = pack
            st.session_state['source_notes'] = notes
            st.session_state['receipt'] = receipt
            st.session_state['generation'] = st.session_state.get('generation', 0) + 1
        except StudyError as error:
            st.error(str(error))

if 'study_pack' not in st.session_state:
    st.divider()
    a,b,c = st.columns(3)
    a.subheader('01 · Understand'); a.write('Three concise summary points.')
    b.subheader('02 · Recall'); b.write('Flashcards with answers you reveal.')
    c.subheader('03 · Check'); c.write('A quiz linked to the original notes.')
else:
    pack = st.session_state['study_pack']
    receipt = st.session_state['receipt']
    st.divider(); st.subheader(pack.title)
    st.caption(f'Generated from the last submitted notes · {receipt["total_tokens"]} total tokens')
    if notes != st.session_state['source_notes']:
        st.info('This result belongs to the previously submitted notes. Submit the form to generate from your edits.')
    summary, cards, quiz, source = st.tabs(['Summary', 'Flashcards', 'Quiz', 'Check sources'])
    with summary:
        for point in pack.summary:
            st.write('• ' + point.text)
            with st.expander(f'Source L{point.evidence.line}'):
                st.text(point.evidence.quote)
    with cards:
        for card in pack.flashcards:
            with st.expander(card.question):
                st.write(card.answer); st.caption(f'Source L{card.evidence.line}: {card.evidence.quote}')
    with quiz:
        generation = st.session_state['generation']
        with st.form(f'quiz_{generation}'):
            answers = [st.radio(q.question, range(3), format_func=lambda i,q=q: q.options[i], index=None,
                        key=f'answer_{generation}_{n}') for n,q in enumerate(pack.quiz)]
            check = st.form_submit_button('Check my answers')
        if check:
            if None in answers:
                st.warning('Answer every question first.')
            else:
                st.session_state['checked_quiz'] = answers
        if 'checked_quiz' in st.session_state:
            answers = st.session_state['checked_quiz']
            score = sum(a == q.correct_index for a,q in zip(answers, pack.quiz))
            st.subheader(f'{score} / 3 against the generated answer key')
            for n,q in enumerate(pack.quiz, 1):
                st.write(f'{n}. {q.options[q.correct_index]} — {q.explanation}')
                st.caption(f'Source L{q.evidence.line}: {q.evidence.quote}')
    with source:
        st.warning('The code checks line numbers and exact quotes. You must still check whether each claim follows from the quote.')
        for n,line in enumerate(prepare_notes(st.session_state['source_notes']), 1):
            st.text(f'L{n}: {line}')
    st.download_button('Download study pack + answer key', to_markdown(pack), 'study-pack.md', 'text/markdown')
    st.caption('AI-generated study aid. A correct data format does not guarantee correct facts.')
