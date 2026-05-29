import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:5001/api',
});

export interface SermonDoc {
  id: number;
  title: string;
  fileName: string;
  pageCount: number;
  uploadedAt: string;
  isIndexed: boolean;
  indexedAt: string | null;
}

export interface IndexStatus {
  isRunning: boolean;
  total: number;
  completed: number;
  failed: number;
  currentFile: string;
  startedAt: string | null;
  errors: string[];
}

export interface Citation {
  documentTitle: string;
  fileName: string;
  pageNumber: number;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
}

export const getSermonDocs = () => client.get<SermonDoc[]>('/sermon-docs');
export const uploadSermonDoc = (file: File) => {
  const form = new FormData();
  form.append('file', file);
  return client.post<SermonDoc>('/sermon-docs/upload', form);
};
export const reindexSermonDoc = (id: number) => client.post(`/sermon-docs/${id}/reindex`, {});
export const deleteSermonDoc = (id: number) => client.delete(`/sermon-docs/${id}`);
export const indexAllSermonDocs = () => client.post<{ message: string; queued: number }>('/sermon-docs/index-all', {});
export const getIndexStatus = () => client.get<IndexStatus>('/sermon-docs/index-status');
export const chatSearch = (question: string) => client.post<ChatResponse>('/search/chat', { question });
