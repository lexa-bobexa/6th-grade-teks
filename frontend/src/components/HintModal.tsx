import * as Dialog from '@radix-ui/react-dialog'

export function HintModal({ open, onOpenChange, hints }: { open: boolean; onOpenChange: (v: boolean) => void; hints: string[] }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)' }} />
        <Dialog.Content className="fade-in" style={{ position: 'fixed', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', background: '#1e293b', color: '#e2e8f0', borderRadius: 12, width: 'min(480px, 90vw)', padding: 24, border: '1px solid #334155', boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.4)' }}>
          <Dialog.Title style={{ fontWeight: 600, marginBottom: 16, fontSize: 18, color: '#3b82f6' }}>💡 Hint</Dialog.Title>
          <ol style={{ margin: 0, paddingLeft: 20, lineHeight: 1.7 }}>
            {hints.slice(0, 3).map((h, i) => (
              <li key={i} style={{ marginBottom: 10, color: '#cbd5e1' }}>{h}</li>
            ))}
          </ol>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 20 }}>
            <Dialog.Close asChild>
              <button type="button">Close</button>
            </Dialog.Close>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}


