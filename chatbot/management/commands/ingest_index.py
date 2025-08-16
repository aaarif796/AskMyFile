from django.core.management.base import BaseCommand
from django.conf import settings
from documents.models import Document  # adjust import
from chatbot.embeddings import (
    load_text_from_file, split_into_passages,
    embed_passages, build_faiss_index
)

import numpy as np
class Command(BaseCommand):
    help = "Ingest and index all documents"

    def handle(self, *args, **options):
        all_texts, all_meta = [], []
        for doc in Document.objects.all():
            path = doc.file.path
            text = load_text_from_file(path)
            passages = split_into_passages(text)
            embeddings = embed_passages(passages)
            for idx, emb in enumerate(embeddings):
                all_texts.append(emb)
                all_meta.append({
                    'doc_id': doc.id,
                    'page': idx,
                    'text': passages[idx],
                })

        embeddings_array = np.vstack(all_texts)
        build_faiss_index(embeddings_array, all_meta)
        self.stdout.write(self.style.SUCCESS("Indexed {} passages".format(len(all_meta))))
